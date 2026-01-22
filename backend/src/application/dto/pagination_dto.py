from pydantic import BaseModel
from typing import Optional, Generic, TypeVar, List

T = TypeVar("T")

class PaginationDTO(BaseModel):
  skip: int = 0
  limit: int = 10
  search: Optional[str] = None

class PaginationResponseDTO(BaseModel, Generic[T]):
  total: int
  skip: int
  limit: int
  items: List[T]