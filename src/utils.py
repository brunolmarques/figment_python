import json
import gzip
from typing import Any, Dict, Iterator
from pathlib import Path

def load_json(path: str) -> Any:
    with open(path, "r") as f:
        return json.load(f)

def save_json(data: Any, path: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def chunked(iterable, size):
    """Yield successive `size`-sized chunks from iterable."""
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]

def read_jsonl_gz(file_path: str | Path) -> Iterator[Dict]:
    """
    Read a gzipped JSONL file line by line.
    Args:
        file_path: Path to the .jsonl.gz file
    Yields:
        Dictionary containing the JSON data from each line
    """
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                yield json.loads(line)

def read_validators_data(batch_size: int = 1000) -> Iterator[list[Dict]]:
    """
    Read the validators data in batches.
    Args:
        batch_size: Number of records to yield at once
    Yields:
        List of dictionaries containing validator data
    """
    data_path = Path("input_data/validators_data.jsonl.gz")
    batch = []

    for record in read_jsonl_gz(data_path):
        batch.append(record)
        if len(batch) >= batch_size:
            yield batch
            batch = []
