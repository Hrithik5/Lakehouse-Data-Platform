import logging
from pathlib import Path

# ------------------------------------------------------------------
# Log Directory
# ------------------------------------------------------------------

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

# ------------------------------------------------------------------
# Logger Configuration
# ------------------------------------------------------------------

logger = logging.getLogger("etl_pipeline")

logger.setLevel(logging.INFO)

# Avoid duplicate handlers when importing multiple times
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s"
    )

    # Console Logger
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Logger
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# Prevent duplicate logging from parent logger
logger.propagate = False