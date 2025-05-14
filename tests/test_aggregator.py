import pytest
import polars as pl
from src.aggregator import (
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
