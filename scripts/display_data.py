import polars as pl
import argparse
from src.utils import read_validators_data
from src.logger import init_logger, logger

# Initialize logger
init_logger(log_level="INFO")

def display_top_rows(n: int = 10) -> None:
    """
    Read the input data and display the top n rows.
    
    Args:
        n: Number of rows to display
    """
    try:
        # Read data in batches and convert to DataFrame
        dfs = []
        for batch in read_validators_data(batch_size=n):
            df = pl.DataFrame(batch)
            dfs.append(df)
            if len(dfs) * len(batch) >= n:
                break
        
        # Combine DataFrames and take top n rows
        combined_df = pl.concat(dfs)
        top_n_df = combined_df.head(n)
        
        # Display DataFrame info and content
        print("\nData Preview:")
        print(top_n_df)
    
        
    except Exception as e:
        logger.error(f"Error reading data: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Display top N rows of validator data")
    parser.add_argument(
        "-n", "--num-rows",
        type=int,
        default=10,
        help="Number of rows to display (default: 10)"
    )
    args = parser.parse_args()
    display_top_rows(args.num_rows) 