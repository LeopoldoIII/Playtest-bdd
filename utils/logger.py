import logging
import os
from datetime import datetime

class Logger:
    @staticmethod
    def setup_logger(name="PlaytestBDD"):
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a unique log file for the execution
        log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_execution.log"
        log_filepath = os.path.join(log_dir, log_filename)

        logger = logging.getLogger(name)
        
        # If logger already has handlers, don't add them again (prevents duplicate logs)
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            # Create handlers
            c_handler = logging.StreamHandler()
            f_handler = logging.FileHandler(log_filepath)

            c_handler.setLevel(logging.INFO)
            f_handler.setLevel(logging.DEBUG)

            # Create formatters and add it to handlers
            c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            logger.addHandler(c_handler)
            logger.addHandler(f_handler)

        return logger
