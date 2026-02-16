
class AuthException(Exception):
  """Base class for authentication exceptions."""
  def __init__(self, message: str):
    super().__init__(message)