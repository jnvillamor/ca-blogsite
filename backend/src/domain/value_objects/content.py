from typing import Any

from src.domain.exceptions import InvalidDataException

class Content:
  def __init__(
    self,
    value: list[dict[str, Any]],
  ):
    if not isinstance(value, list):
      raise InvalidDataException("Content must be a JSON array of block objects.")
    if len(value) == 0:
      raise InvalidDataException("Content cannot be empty.")
    self.value = value
