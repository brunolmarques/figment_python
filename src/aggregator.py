import polars as pl
from typing import Dict, Any, List
from src.utils import read_validators_data


def jsonl_to_dataframe(batch_size: int = 1000) -> pl.DataFrame:
    """
    Convert JSONL data to Polars DataFrame.
    Args:
        batch_size: Number of records to process at once
    Returns:
        Polars DataFrame containing all validator data
    """
    # Initialize empty list to store DataFrames
    dfs: List[pl.DataFrame] = []
    
    # Process data in batches
    for batch in read_validators_data(batch_size):
        # Convert batch to DataFrame
        df = pl.DataFrame(batch)
        dfs.append(df)
    
    # Concatenate all DataFrames
    return pl.concat(dfs)


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
        df
        .group_by("block_number")
        .agg(pl.col("effective_balance").sum().alias("total_effective_balance"))
    )


def block_slashed_count(df: pl.DataFrame) -> pl.DataFrame:
    """
    Count slashed validators per block.
    """
    return (
        df
        .filter(pl.col("slashed") == 1)
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


def compute_block_stats(df: pl.DataFrame) -> Dict[str, Dict[str, Any]]:
    """
    Compute all per-block statistics and return a nested dict:
    { block_number: { balance, effective_balance, slashed, <status_counts> } }
    """
    bal_df = block_balance(df)
    eff_df = block_effective_balance(df)
    sl_df = block_slashed_count(df)
    st_df = block_status_counts(df)

    # Left join all metrics on block_number
    merged = (
        bal_df
        .join(eff_df, on="block_number")
        .join(sl_df, on="block_number", how="left")
        .join(st_df, on="block_number", how="left")
        .fill_null(0)
    )

    # Convert to nested dictionary
    result: Dict[str, Dict[str, Any]] = {}
    for row in merged.iter_rows(named=True):
        blk = str(row["block_number"])
        # extract metrics
        block_data = {
            "balance": row["total_balance"],
            "effective_balance": row["total_effective_balance"],
            "slashed": int(row.get("slashed_count", 0)),
        }
        # include status counts (all other keys)
        status_keys = set(row.keys()) - {"block_number", "total_balance", "total_effective_balance", "slashed_count"}
        for key in status_keys:
            block_data[key] = int(row[key])
        result[blk] = block_data
    return result


def compute_totals(blocks: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Sum totals across all blocks. Returns a flat dict with keys:
    balance, effective_balance, slashed, plus aggregated status counts.
    """
    total_balance = sum(b["balance"] for b in blocks.values())
    total_effective = sum(b["effective_balance"] for b in blocks.values())
    total_slashed = sum(b["slashed"] for b in blocks.values())

    status_totals: Dict[str, int] = {}
    for b in blocks.values():
        for k, v in b.items():
            if k in ("balance", "effective_balance", "slashed"):  # skip numeric metrics
                continue
            status_totals[k] = status_totals.get(k, 0) + v

    return {
        "balance": total_balance,
        "effective_balance": total_effective,
        "slashed": total_slashed,
        **status_totals,
    }
