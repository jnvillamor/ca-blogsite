from pydantic import BaseModel
from typing import Optional

class PaginationDTO(BaseModel):
  skip: int
  limit: int
  search: Optional[str] = None