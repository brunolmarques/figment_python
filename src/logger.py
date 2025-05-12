from loguru import logger
import sys
from pathlib import Path

def init_logger(
    log_level: str = "INFO",
    log_file: str | Path | None = None,
    rotation: str = "500 MB",
    retention: str = "10 days",
) -> None:
    """
    Initialize the logger with custom configuration.
    
    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the log file. If None, logs only to console
        rotation: When to rotate the log file (e.g., "500 MB", "1 day")
        retention: How long to keep rotated logs (e.g., "10 days", "1 week")
    
    Usage:
        1. Initialize once at startup:
            init_logger(log_level="INFO", log_file="logs/app.log")

        2. Log messages:
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            logger.critical("Critical message")

        3. Log exceptions:
            try:
                # code
            except Exception as e:
                logger.exception("Error occurred")
    """

    logger.remove()
    
    # Add console handler with custom format
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )
    
    # Add file handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_path,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level,
            rotation=rotation,
            retention=retention,
            compression="zip",
        )

