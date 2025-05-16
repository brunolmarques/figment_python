from src.config import (
    LOG_LEVEL, LOG_DIR, INPUT_PATH, OUTPUT_DIR,
    BLOCK_FILES, TOTAL_FILES
)
from src.logger import init_logger, logger
from src.aggregator import load_validators, compute_block_stats, compute_totals
from src.utils import save_json

def main():
    # Initialize logger
    init_logger(log_level=LOG_LEVEL, log_file=LOG_DIR / "aggregator.log")
    logger.info("Starting data processing")

    try:
        # Read data as LazyFrame for memory-efficient processing
        logger.info(f"Reading input data from {INPUT_PATH}")
        lazy_df = load_validators(INPUT_PATH)
        logger.info("Data loaded as LazyFrame")
        
        # Process data using lazy evaluation
        logger.info("Computing block statistics")
        block_stats = compute_block_stats(lazy_df)
        logger.info(f"Processed {len(block_stats)} blocks")

        # Compute totals
        logger.info("Computing totals")
        totals = compute_totals(block_stats)
        logger.info("Totals computed successfully")

        # Create output directory
        OUTPUT_DIR.mkdir(exist_ok=True)

        # Save block statistics
        for metric, file_path in BLOCK_FILES.items():
            metric_data = {block: stats[metric] for block, stats in block_stats.items()}
            save_json(metric_data, file_path)
            logger.info(f"Saved {metric} block statistics to {file_path}")

        # Save totals
        for metric, file_path in TOTAL_FILES.items():
            metric_total = {metric: totals[metric]}
            save_json(metric_total, file_path)
            logger.info(f"Saved {metric} total to {file_path}")

        logger.info("Data processing completed successfully")

    except Exception:
        logger.exception("Error during data processing")
        raise

if __name__ == "__main__":
    main()

