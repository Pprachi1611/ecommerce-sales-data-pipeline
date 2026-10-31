from logger_config import get_logger

logger = get_logger("TEST")

logger.info("Logging system initialized successfully.")
logger.warning("This is a sample warning.")
logger.error("This is a sample error.")