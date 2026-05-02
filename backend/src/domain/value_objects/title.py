from src.domain.exceptions import InvalidDataException

class Title:
  MIN_LENGTH = 5
  MAX_LENGTH = 100

  def __init__(
    self,
    value: str,
  ):
    self.value = (value or "").strip()

  def validate_for_publish(self) -> None:
    if not self.value:
      raise InvalidDataException("Title cannot be empty.")
    if len(self.value) < self.MIN_LENGTH:
      raise InvalidDataException(f"Title must be at least {self.MIN_LENGTH} characters long.")
    if len(self.value) > self.MAX_LENGTH:
      raise InvalidDataException(f"Title cannot exceed {self.MAX_LENGTH} characters.")
