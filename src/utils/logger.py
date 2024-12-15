import logging

__all__ = ['logger']

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Output to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
