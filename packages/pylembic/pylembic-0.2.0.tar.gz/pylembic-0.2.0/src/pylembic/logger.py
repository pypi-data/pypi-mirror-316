import logging

from pylembic.formatter import CustomFormatter


def configure_logger(verbose: bool = False):
    """Configure the logger with a custom formatter and verbosity level.

    Args:
        verbose (bool): Whether to enable verbose logging.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger()

    if not verbose:
        logger.setLevel(logging.CRITICAL + 1)
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = CustomFormatter(
        "%(levelname)s\t %(asctime)s | %(message)s | %(migration)s"
        "%(dependency)s%(orphans)s%(heads)s%(bases)s",
        datefmt="%d %b %Y | %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
