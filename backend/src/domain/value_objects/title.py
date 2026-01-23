from src.domain.exceptions import InvalidDataException

class Title:
  def __init__(
    self,
    value: str,
  ):
    if not value or not value.strip():
      raise InvalidDataException("Title cannot be empty.")
    if len(value) < 5:
      raise InvalidDataException("Title must be at least 5 characters long.")
    if len(value) > 100:
      raise InvalidDataException("Title cannot exceed 100 characters.")
    self.value = value.strip()