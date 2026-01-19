class InvalidDataException(Exception):
  def __init__(self, message: str):
    super().__init__(message)

class NotFoundException(Exception):
  def __init__(self, entity_name: str, identifier: str):
    message = f"{entity_name} with identifier '{identifier}' was not found."
    super().__init__(message)
