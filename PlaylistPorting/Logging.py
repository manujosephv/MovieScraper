
import logging
from Singleton import Singleton

class Logging:
    
    __metaclass__ = Singleton
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)