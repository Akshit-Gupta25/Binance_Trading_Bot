import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(name: str = "trading_bot") -> logging.Logger:
    logs_dir = Path(__file__).resolve().parent.parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "trading_bot.log"
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(str(log_file), maxBytes=2_000_000, backupCount=3, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

