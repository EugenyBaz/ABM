import sys

from loguru import logger


def setup_logging() -> None:
    """
    Настройка логирования приложения.

    Конфигурирует Loguru:
    - вывод логов в консоль
    - запись логов в файл с ротацией и хранением
    """
    logger.remove()  # убираем дефолтный sink

    # Логи в консоль
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan> | {message}",
    )

    # Логи в файл
    logger.add(
        "logs/app.log",
        rotation="1 MB",
        retention="10 days",
        level="INFO",
        format="{time} | {level} | {name} | {message}",
    )
