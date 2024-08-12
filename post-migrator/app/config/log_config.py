import logging
import os


def setup_logger(log_file='app.log'):
    """
    Setup the logger for the application.
    """
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_file)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(
                filename=log_path,
                mode='a',
                encoding='utf-8'
            ),
            logging.StreamHandler()
        ]
    )

    # Create and return logger with module name granularity
    return logging.getLogger(__name__)

# Initialize the logger as a global variable
logger = setup_logger()
