import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more verbose output
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler('financeai.log', mode='a') 
    ]
)

# Create a logger for this module
logger = logging.getLogger(__name__)
