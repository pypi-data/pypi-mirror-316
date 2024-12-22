import logging
from .args import args_client
log_client = None

def init_logger():
    global log_client
    log_client = logging.getLogger(__name__)
    verbosity_levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG
    }
    logging.basicConfig()
    log_client.setLevel(verbosity_levels.get(args_client.verbosity, logging.INFO))