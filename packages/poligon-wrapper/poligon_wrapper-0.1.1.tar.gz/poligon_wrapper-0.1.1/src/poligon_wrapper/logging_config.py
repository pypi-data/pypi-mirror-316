import logging
import os

def setup_logging(log_file='./logs/project.log', level=logging.DEBUG):
    # Create a directory for logs if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),  # Log to file
            logging.StreamHandler()          # Log to console
        ]
    )
