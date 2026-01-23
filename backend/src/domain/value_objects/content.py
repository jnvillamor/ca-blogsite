from src.domain.exceptions import InvalidDataException

class Content:
  def __init__(
    self,
    value: str,
  ):
    if not value or not value.strip():
      raise InvalidDataException("Content cannot be empty.")
    self.value = value.strip()