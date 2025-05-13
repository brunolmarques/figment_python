import pytest
import polars as pl
from src.aggregator import (
    block_balance,
    block_effective_balance,
    block_slashed_count,
    block_status_counts,
    compute_block_stats,
    compute_totals
)

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pl.DataFrame({
        "block_number": [1, 1, 2, 2, 3],
        "balance": [100, 200, 300, 400, 500],
        "slashed": [0, 1, 0, 0, 1],
        "status": ["active", "exited_slashed", "active", "pending", "exited_slashed"]
    })

def test_block_balance(sample_df):
    """Test block balance aggregation."""
    result = block_balance(sample_df)
    
    # Check structure
    assert "block_number" in result.columns
    assert "total_balance" in result.columns
    
    # Check values
    expected = {
        1: 300,  # 100 + 200
        2: 700,  # 300 + 400
        3: 500   # 500
    }
    
    for row in result.iter_rows(named=True):
        assert row["total_balance"] == expected[row["block_number"]]

def test_block_effective_balance(sample_df):
    """Test block effective balance aggregation."""
    # Convert to LazyFrame for compatibility with aggregator implementation
    result = block_effective_balance(sample_df.lazy())
    
    columns = result.collect_schema().names()
    
    # Check structure
    assert "block_number" in columns
    assert "effective_balance" in columns
    
    # Check values (should match the capped/floored balance logic)
    expected = {
        1: 0,  # 100 + 200 floored to 0 (since < 1e9 Gwei)
        2: 0,  # 300 + 400 floored to 0
        3: 0   # 500 floored to 0
    }
    for row in result.collect().iter_rows(named=True):
        assert row["effective_balance"] == expected[row["block_number"]]

def test_block_slashed_count(sample_df):
    """Test slashed validator counting."""
    result = block_slashed_count(sample_df)
    
    # Check structure
    columns = result.collect_schema().names()
    assert "block_number" in columns
    assert "slashed_count" in columns
    
    # Check values
    expected = {
        1: 1,  # One slashed validator
        3: 1   # One slashed validator
    }
    
    for row in result.iter_rows(named=True):
        assert row["slashed_count"] == expected[row["block_number"]]

def test_block_status_counts(sample_df):
    """Test status counting and pivoting."""
    result = block_status_counts(sample_df)
    
    # Check structure
    columns = result.collect_schema().names()
    assert "block_number" in columns
    assert "active" in columns
    assert "exited_slashed" in columns
    assert "pending" in columns
    
    # Check values
    expected = {
        1: {"active": 1, "exited_slashed": 1, "pending": 0},
        2: {"active": 1, "exited_slashed": 0, "pending": 1},
        3: {"active": 0, "exited_slashed": 1, "pending": 0}
    }
    
    for row in result.iter_rows(named=True):
        block = row["block_number"]
        assert row["active"] == expected[block]["active"]
        assert row["exited_slashed"] == expected[block]["exited_slashed"]
        assert row["pending"] == expected[block]["pending"]

def test_compute_block_stats(sample_df):
    """Test complete block statistics computation."""
    # Convert to LazyFrame for compatibility with aggregator implementation
    result = compute_block_stats(sample_df.lazy())
    
    # Check structure
    assert "1" in result
    assert "2" in result
    assert "3" in result
    
    # Check block 1
    block1 = result["1"]
    assert block1["balance"] == 300
    assert block1["slashed"] == 1
    assert block1["status"].get("active", 0) == 1

def test_compute_totals(sample_df):
    """Test totals computation."""
    # Convert to LazyFrame for compatibility with aggregator implementation
    block_stats = compute_block_stats(sample_df.lazy())
    result = compute_totals(block_stats)
    
    # Check totals
    assert result["balance"] == 1500
    assert result["slashed"] == 2
    assert result["status"].get("active", 0) == 2
    assert result["status"].get("pending", 0) == 1

# def test_jsonl_to_dataframe():
#     """Test DataFrame conversion from JSONL."""
#     # This test might need to be skipped in CI or modified to use test data
#     try:
#         df = jsonl_to_dataframe(batch_size=1000)
#         assert isinstance(df, pl.DataFrame)
#         assert len(df) > 0
#         assert "block_number" in df.columns
#         assert "balance" in df.columns
#         assert "effective_balance" in df.columns
#         assert "slashed" in df.columns
#         assert "status" in df.columns
#     except FileNotFoundError:
#         pytest.skip("Input data file not found")
