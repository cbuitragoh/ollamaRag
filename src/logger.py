import logging

# create and configure logger

def create_logger(__name__:str | None = None):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    
    return logger