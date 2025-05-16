import polars as pl
from typing import Dict, Any

# constants in Gwei
MAX_EFFECTIVE = 32_000_000_000
INCREMENT     =  1_000_000_000
BUFFER_CONST_GWEI = 0.25  # Buffer of 0.25 ETH in Gwei

# Validator statuses
VALIDATOR_STATUSES = [
    "withdrawal_done",
    "active_slashed",
    "exited_unslashed",
    "active_ongoing",
    "active_exiting",
    "pending_queued",
    "withdrawal_possible",
    "pending_initialized",
    "exited_slashed"
]


def load_validators(path: str) -> pl.LazyFrame:
    """
    Load validators data as a LazyFrame for memory-efficient processing.
    """
    return (
        pl.scan_ndjson(path)
        .with_columns([
            pl.col("index").cast(pl.Int64),
            pl.col("balance").cast(pl.Float64),
            pl.col("status").cast(pl.Utf8),
            pl.col("validator").cast(pl.Utf8),
            pl.col("block_number").cast(pl.Int64),
        ])
    )

def compute_block_stats(lazy_df: pl.LazyFrame) -> Dict[str, Dict[str, Any]]:
    # Chain all operations in a single expression
    merged = (
        lazy_df
        .with_columns([
            (
                (pl.col("balance").clip(upper_bound=MAX_EFFECTIVE) / INCREMENT) # Cap, then divide by INCREMENT
                .floor()                                                       # Floor to nearest whole number (of INCREMENTs)
                * INCREMENT                                                    # Multiply back by INCREMENT
            ).alias("effective_balance")
        ])
        # Then group and aggregate
        .group_by("block_number")
        .agg([
            # Calculate balance with 9 decimal precision
            pl.col("balance").sum().cast(pl.Float64).map_elements(lambda x: float(f"{x:.9e}"), return_dtype=pl.Float64).alias("total_balance"),
            # Calculate effective balance with 6 decimal precision (scientific notation)
            pl.col("effective_balance").sum().cast(pl.Float64).map_elements(lambda x: float(f"{x:.6e}"), return_dtype=pl.Float64).alias("total_effective_balance"),
            # Calculate slashed count
            pl.col("status")
              .filter(pl.col("status").str.contains("_slashed"))
              .len()
              .alias("slashed_count"),
            # Calculate status counts
            pl.col("status")
              .value_counts()
              .alias("status_counts"),
        ])
        .collect(engine="streaming")
    )

    result: Dict[str, Dict[str, Any]] = {}
    for row in merged.iter_rows(named=True):
        blk = str(row["block_number"])
        status_counts = row["status_counts"]

        # base metrics
        block_data = {
            "balance":               row["total_balance"],  
            "effective_balance":     row["total_effective_balance"],  
            "slashed":               int(row["slashed_count"]),
            "status":               {status: 0 for status in VALIDATOR_STATUSES}
        }

        # Update with actual counts
        for rec in status_counts:
            name  = rec.get("status")
            count = rec.get("count")
            if name is not None and count is not None and name in VALIDATOR_STATUSES:
                block_data["status"][name] = int(count)
        
        result[blk] = block_data
    
    return result


def compute_totals(blocks: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Sum totals across all blocks. Returns a flat dict with keys:
    balance, effective_balance, slashed, plus aggregated status counts.
    """
    # Convert blocks dict to a Polars DataFrame for efficient aggregation
    df = pl.DataFrame([
        {
            "balance": b["balance"],
            "effective_balance": b["effective_balance"],
            "slashed": b["slashed"],
            **{f"status_{k}": b["status"].get(k, 0) for k in VALIDATOR_STATUSES}
        }
        for b in blocks.values()
    ])

    # Chain aggregations with proper decimal precision
    totals = (
        df
        .select([
            pl.col("balance").sum().cast(pl.Float64).map_elements(lambda x: float(f"{x:.9e}"), return_dtype=pl.Float64).alias("balance"),
            pl.col("effective_balance").sum().cast(pl.Float64).map_elements(lambda x: float(f"{x:.6e}"), return_dtype=pl.Float64).alias("effective_balance"),
            pl.col("slashed").sum().alias("slashed"),
            *[pl.col(f"status_{status}").sum().alias(status) for status in VALIDATOR_STATUSES]
        ])
    ).row(0, named=True)

    # Initialize status_counts with all keys from VALIDATOR_STATUSES, default to 0
    status_counts = {status: 0 for status in VALIDATOR_STATUSES}
    # Update with values from Polars aggregation if they exist
    for status_name in VALIDATOR_STATUSES:
        if status_name in totals:
            status_counts[status_name] = totals[status_name]
    
    other_totals = {k: v for k, v in totals.items() if k not in VALIDATOR_STATUSES}

    return {
        **other_totals,
        "status": status_counts
    }
