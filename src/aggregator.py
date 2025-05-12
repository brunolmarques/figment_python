import subprocess, tempfile
import polars as pl
from typing import Dict, Any, List

# constants in Gwei
MAX_EFFECTIVE = 32_000_000_000
INCREMENT     =  1_000_000_000

def load_validators(path: str) -> pl.DataFrame:
    """
    Loads a newline-delimited JSON (.json.gz) of Ethereum validators
    in parallel using Polars' scan_json API.
    """
    # decompress with pigz (much faster than gzip) into a temp file
    with tempfile.NamedTemporaryFile(suffix=".ndjson", delete=False) as tmp:
        subprocess.run(["pigz", "-dc", path], stdout=tmp, check=True)
        tmp_path = tmp.name

        # now scan lazily (parallel) from the decompressed NDJSON
        return (
            pl.scan_ndjson(path)
            .with_columns([
                pl.col("index").cast(pl.Int64),
                pl.col("balance").cast(pl.Float64),
                pl.col("status").cast(pl.Utf8),
                pl.col("validator").cast(pl.Utf8),
                pl.col("block_number").cast(pl.Int64),
            ])
            .collect()  # triggers parallel execution
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
              .clip_max(MAX_EFFECTIVE)         # cap at 32 ETH
              .floor_div(INCREMENT)            # how many whole ETH
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
        .groupby("block_number")
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
