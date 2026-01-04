from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
  @abstractmethod
  def hash(self, password: str) -> str:
    """Hash the given password

    Args:
      password (str): plain user password

    Returns:
      str: returns the hashed password
    """
    pass
  
  @abstractmethod
  def verify(self, password: str, hashed_password: str) -> bool:
    """Verify the given password against the hashed password

    Args:
      password (str): plain user password
      hashed_password (str): hashed user password

    Returns:
      bool: returns True if the password matches the hashed password, False otherwise
    """
    pass
