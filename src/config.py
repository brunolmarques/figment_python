from pathlib import Path

LOG_LEVEL = "INFO"
LOG_DIR = Path("logs")
INPUT_PATH  = Path("input_data/validators_data.jsonl.gz")
OUTPUT_DIR  = Path("output")
BLOCK_FILES = {
    "balance": OUTPUT_DIR / "balance_block.json",
    "effective_balance": OUTPUT_DIR / "effective_balance_block.json",
    "slashed": OUTPUT_DIR / "slashed_block.json",
    "status": OUTPUT_DIR / "status_block.json",
}
TOTAL_FILES = {
    "balance": OUTPUT_DIR / "balance_total.json",
    "effective_balance": OUTPUT_DIR / "effective_balance_total.json",
    "slashed": OUTPUT_DIR / "slashed_total.json",
    "status": OUTPUT_DIR / "status_total.json",
}
