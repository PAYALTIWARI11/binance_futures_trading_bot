import logging
import os
import sys

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

MARKET_LOG_FILE = os.path.join(LOG_DIR, 'market_order.log')
LIMIT_LOG_FILE = os.path.join(LOG_DIR, 'limit_order.log')

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(module)s | %(message)s')

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    # Also log to console (stdout) specifically for general feedback if needed, 
    # but the prompt asked for separate files. We'll add a StreamHandler to the root 
    # or specific loggers if we want console output too. 
    # For this assignment, "Output to console" is a requirement for order summary vs logs.
    # We will keep logs clean and strictly file-based for the requirement "Ensure logs are NOT noisy",
    # but "Errors & exceptions" should probably be visible?
    # Let's add a console handler to the root logger just in case, but keep it quiet?
    # Actually, prompt says "Output to console: Order request summary...". 
    # This suggests `print` or specific console logging.
    # I will return the logger instance.
    
    return logger

# Create specific loggers
market_logger = setup_logger('market_logger', MARKET_LOG_FILE)
limit_logger = setup_logger('limit_logger', LIMIT_LOG_FILE)

# General application logger (can share one of the files or be separate, keeping it simple mapped to functionality)
def get_logger(order_type=None):
    if order_type == 'MARKET':
        return market_logger
    elif order_type == 'LIMIT':
        return limit_logger
    else:
        # Default fallback, maybe just log to one or both? 
        # For general app errors not specific to an order type, let's use market_order.log for now or a general approach.
        return market_logger
