from src.domain.exceptions import InvalidDataException

class Name:
  def __init__(
    self,
    value: str,
    type: str = "Name",
    min_length: int = 2,
    max_length: int = 50
  ):
    if not value or not value.strip():
      raise InvalidDataException(f"{type} cannot be empty.")
    if len(value) < min_length:
      raise InvalidDataException(f"{type} must be at least {min_length} characters long.")
    if len(value) > max_length:
      raise InvalidDataException(f"{type} cannot exceed {max_length} characters.")
    self.value = value.strip()
    
  def __eq__(self, other):
    if isinstance(other, Name):
      return self.value == other.value
    return False

class FirstName(Name):
  def __init__(self, value: str):
    super().__init__(value, type="First Name", min_length=2, max_length=30)

class LastName(Name):
  def __init__(self, value: str):
    super().__init__(value, type="Last Name", min_length=2, max_length=30)
    
class Username(Name):
  def __init__(self, value: str):
    super().__init__(value, type="Username", min_length=3, max_length=20)      
    