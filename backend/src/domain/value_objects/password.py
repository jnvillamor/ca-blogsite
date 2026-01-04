from src.domain.exceptions import InvalidDataException

class Password:
  def __init__(self, hashed_password: str):
    self.value = hashed_password
    
  def __eq__(self, other):
    if isinstance(other, Password):
      return self.value == other.value
    return False
  
  @staticmethod
  def is_valid(plain_password: str) -> bool:
    if not plain_password:
      raise InvalidDataException("Password cannot be empty.")
    if len(plain_password) < 8:
      raise InvalidDataException("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in plain_password):
      raise InvalidDataException("Password must contain at least one digit.")
    if not any(char.isupper() for char in plain_password):
      raise InvalidDataException("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in plain_password):
      raise InvalidDataException("Password must contain at least one lowercase letter.")
    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in plain_password):
      raise InvalidDataException("Password must contain at least one special character.")
    return True
  