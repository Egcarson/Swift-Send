import logging

# Set up logger as a global variable
logging.basicConfig(
     level=logging.INFO,
     format='%(module)s %(levelname)s %(message)s %(asctime)s '
     )

def get_logger():
    logger = logging.getLogger()
    return logger

