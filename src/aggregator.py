import polars as pl
from typing import Dict, Any

# constants in Gwei
MAX_EFFECTIVE = 32_000_000_000
INCREMENT     =  1_000_000_000

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


def with_effective_balance(df: pl.DataFrame) -> pl.DataFrame:
    """
    Adds a column `effective_balance` to `df` by:
      1. capping each `balance` at 32 ETH (32e9 Gwei),
      2. flooring to the nearest 1 ETH (1e9 Gwei) increment,
      3. leaving other columns untouched.
    """
    return df.with_columns([
        (
            pl.col("balance")
              .clip(None, MAX_EFFECTIVE)         # cap at 32 ETH
              .floordiv(INCREMENT)            # how many whole ETH
              * INCREMENT                      # back to Gwei
        ).alias("effective_balance")
    ])

def block_balance(df: pl.DataFrame) -> pl.DataFrame:
    """
    Sum validator balances per block.
    """
    return (
        df
        .group_by("block_number")
        .agg(pl.col("balance").sum().alias("total_balance"))
    )


def block_effective_balance(df: pl.DataFrame) -> pl.DataFrame:
    """
    Sum validator effective balances per block.
    """
    return (
        with_effective_balance(df)
        .group_by("block_number")
        .agg(
            pl.sum("effective_balance").alias("effective_balance")
        )
    )


def block_slashed_count(df: pl.DataFrame) -> pl.DataFrame:
    """
    Count slashed validators per block.
    """
    return (
        df
        .filter(pl.col("status") == "exited_slashed")
        .group_by("block_number")
        .agg(pl.len().alias("slashed_count"))
    )


def block_status_counts(df: pl.DataFrame) -> pl.DataFrame:
    """
    Count validators per status per block, pivoted into columns.
    """
    return (
        df
        .group_by(["block_number", "status"])
        .agg(pl.len().alias("count"))
        .pivot(
            values="count",
            index="block_number",
            on="status",
        )
        .fill_null(0)
    )


def compute_block_stats(lazy_df: pl.LazyFrame) -> Dict[str, Dict[str, Any]]:
    merged = (
        lazy_df
        .group_by("block_number")
        .agg([
            pl.col("balance").sum().alias("total_balance"),
            (pl.col("balance")
               .clip(None, MAX_EFFECTIVE)
               .floordiv(INCREMENT)
               * INCREMENT
            ).sum().alias("total_effective_balance"),
            pl.col("status")
              .filter(pl.col("status") == "exited_slashed")
              .len()
              .alias("slashed_count"),
            pl.col("status")
              .value_counts()
              .alias("status_counts"),
        ])
        .collect(engine="streaming")
    )

    result: Dict[str, Dict[str, Any]] = {}
    for row in merged.iter_rows(named=True):
        blk = str(row["block_number"])
        status_counts = row["status_counts"]  # this is a Python list of structs/dicts

        # base metrics
        block_data = {
            "balance":               row["total_balance"],
            "effective_balance":     row["total_effective_balance"],
            "slashed":               int(row["slashed_count"]),
        }

        # build a nested status map instead of flattening
        status_map: Dict[str,int] = {}
        for rec in status_counts:
            name  = rec.get("status")
            count = rec.get("count")
            if name is not None and count is not None:
                status_map[name] = int(count)
        block_data["status"] = status_map
        
        result[blk] = block_data
        
    return result


def compute_totals(blocks: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Sum totals across all blocks. Returns a flat dict with keys:
    balance, effective_balance, slashed, plus aggregated status counts.
    """
    total_balance   = sum(b["balance"]            for b in blocks.values())
    total_effective = sum(b["effective_balance"]  for b in blocks.values())
    total_slashed   = sum(b["slashed"]            for b in blocks.values())

    status_totals: Dict[str, int] = {}

    # Only aggregate the nested status maps
    status_totals: Dict[str, int] = {}
    for b in blocks.values():
        status_map = b.get("status", {})
        for name, count in status_map.items():
            status_totals[name] = status_totals.get(name, 0) + count

    return {
        "balance":           total_balance,
        "effective_balance": total_effective,
        "slashed":           total_slashed,
        "status":            status_totals,
    }
