import logging
from .weather import get_weather

__all__ = ["get_weather"]  # Explicitly declare public symbols

# Configure logging for the package
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
