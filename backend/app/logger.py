import logging
from enum import StrEnum

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s | %(filename)s:%(funcName)s:%(lineno)d"

handler = logging.StreamHandler()

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

class LogLevels(StrEnum):
  debug = "DEBUG"
  info = "INFO"
  warning = "WARNING"
  error = "ERROR"
  
def setup_logging(level: str = LogLevels.error) -> None:
  log_level = str(level).upper()
  log_levels = [level.value for level in LogLevels]

  if log_level not in log_levels:
    logging.basicConfig(level=logging.ERROR)
    return
  
  if log_level == LogLevels.debug:
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
  
  logging.basicConfig(level=log_level)