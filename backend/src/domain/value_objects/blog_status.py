from src.domain.exceptions import InvalidDataException

class BlogStatus:
  DRAFT = "draft"
  PUBLISHED = "published"
  ALLOWED = (DRAFT, PUBLISHED)

  def __init__(
    self,
    value: str,
  ):
    if value not in self.ALLOWED:
      raise InvalidDataException(
        f"Invalid blog status '{value}'. Must be one of: {', '.join(self.ALLOWED)}."
      )
    self.value = value
