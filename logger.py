import logging

# Create a dedicated logger
logger = logging.getLogger("bypass_bot")
logger.setLevel(logging.INFO)

# File handler (ONLY your logs)
file_handler = logging.FileHandler("bot_usage.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)

# Avoid duplicate handlers
if not logger.handlers:
    logger.addHandler(file_handler)

#  Disable propagation to root logger
logger.propagate = False
