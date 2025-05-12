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
        "effective_balance": [90, 180, 270, 360, 450],
        "slashed": [0, 1, 0, 0, 1],
        "status": ["active", "slashed", "active", "pending", "slashed"]
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
    result = block_effective_balance(sample_df)
    
    # Check structure
    assert "block_number" in result.columns
    assert "total_effective_balance" in result.columns
    
    # Check values
    expected = {
        1: 270,  # 90 + 180
        2: 630,  # 270 + 360
        3: 450   # 450
    }
    
    for row in result.iter_rows(named=True):
        assert row["total_effective_balance"] == expected[row["block_number"]]

def test_block_slashed_count(sample_df):
    """Test slashed validator counting."""
    result = block_slashed_count(sample_df)
    
    # Check structure
    assert "block_number" in result.columns
    assert "slashed_count" in result.columns
    
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
    assert "block_number" in result.columns
    assert "active" in result.columns
    assert "slashed" in result.columns
    assert "pending" in result.columns
    
    # Check values
    expected = {
        1: {"active": 1, "slashed": 1, "pending": 0},
        2: {"active": 1, "slashed": 0, "pending": 1},
        3: {"active": 0, "slashed": 1, "pending": 0}
    }
    
    for row in result.iter_rows(named=True):
        block = row["block_number"]
        assert row["active"] == expected[block]["active"]
        assert row["slashed"] == expected[block]["slashed"]
        assert row["pending"] == expected[block]["pending"]

def test_compute_block_stats(sample_df):
    """Test complete block statistics computation."""
    result = compute_block_stats(sample_df)
    
    # Check structure
    assert "1" in result
    assert "2" in result
    assert "3" in result
    
    # Check block 1
    block1 = result["1"]
    assert block1["balance"] == 300
    assert block1["effective_balance"] == 270
    assert block1["slashed"] == 1
    assert block1["active"] == 1
    assert block1["slashed"] == 1
    assert block1["pending"] == 0

def test_compute_totals(sample_df):
    """Test totals computation."""
    block_stats = compute_block_stats(sample_df)
    result = compute_totals(block_stats)
    
    # Check totals
    assert result["balance"] == 1500  # Sum of all balances
    assert result["effective_balance"] == 1350  # Sum of all effective balances
    assert result["slashed"] == 2  # Total slashed validators
    assert result["active"] == 2  # Total active validators
    assert result["pending"] == 1  # Total pending validators

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
