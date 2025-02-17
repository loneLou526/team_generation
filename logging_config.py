import os
import logging

def setup_logging():
    if not os.path.exists("/bot"):
        os.makedirs("/bot")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join("/bot", "bot.log")),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    return logger
