from abc import ABC, abstractmethod

class IIdGenerator(ABC):
  @abstractmethod
  def generate(self) -> str:
    """Generate a unique identifier

    Returns:
      str: returns a unique identifier as a string
    """
    pass