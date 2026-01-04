class UsernameExistsException(Exception):
  """Exception raised when a username already exists in the system."""
  def __init__(self, username: str):
    super().__init__(f"The username '{username}' is already taken.")