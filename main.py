import asyncio
import logging

from colorlog import ColoredFormatter

from bot import start_polling
from database import init_db
from src.regular_functions import find_inters


handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red"
    }
)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


async def main():
    tasks = [
        init_db(),
        start_polling(),
        find_inters()
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        logging.info("Чат запущен")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Чат остановлен")
