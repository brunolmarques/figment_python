from src.config import (
    LOG_LEVEL, LOG_DIR, INPUT_PATH, OUTPUT_DIR,
    BLOCK_FILES, TOTAL_FILES
)
from src.logger import init_logger, logger
from src.aggregator import jsonl_to_dataframe, compute_block_stats, compute_totals
from src.utils import save_json

def main():
    # Initialize logger
    init_logger(log_level=LOG_LEVEL, log_file=LOG_DIR / "aggregator.log")
    logger.info("Starting data processing")

    try:
        # Read and convert data to DataFrame
        logger.info(f"Reading input data from {INPUT_PATH}")
        df = jsonl_to_dataframe(batch_size=1000)
        logger.info(f"Loaded {len(df)} records")

        # Compute block statistics
        logger.info("Computing block statistics")
        block_stats = compute_block_stats(df)
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
            metric_total = totals[metric]
            save_json(metric_total, file_path)
            logger.info(f"Saved {metric} total to {file_path}")

        logger.info("Data processing completed successfully")

    except Exception:
        logger.exception("Error during data processing")
        raise

if __name__ == "__main__":
    main()

