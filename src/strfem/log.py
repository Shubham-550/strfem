import logging
import logging.config
import os
from pathlib import Path


def setup_controller_logging(log_dir: str = "logs", log_file: str = "controller.log"):
    """
    Configure logging for the Controller class.

    Args:
        log_dir: Directory to store log files
        log_file: Name of the log file
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Full path for log file
    log_path = os.path.join(log_dir, log_file)

    # Logging configuration dictionary
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "file_handler": {
                "class": "logging.FileHandler",
                "filename": log_path,
                "mode": "a",  # append mode
                "formatter": "standard",
                "encoding": "utf-8",
            }
        },
        "loggers": {
            "controller_logger": {
                "handlers": ["file_handler"],
                "level": "INFO",
                "propagate": False,
            }
        },
    }

    # Configure logging
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("controller_logger")

    # Add a separation line at the start of each script run
    logger.info("\n")
    logger.info("=" * 80)
    logger.info("New script execution started\n")
    return logger
    # return logging.getLogger("controller_logger")
