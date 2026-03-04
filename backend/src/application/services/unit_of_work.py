from abc import ABC, abstractmethod
from src.application.repositories import (
  IUserRepository,
  IBlogRepository
)

class IUnitOfWork(ABC):
  users: IUserRepository
  blogs: IBlogRepository
  
  @abstractmethod
  async def __aenter__(self) -> 'IUnitOfWork':
    pass
  
  @abstractmethod
  async def __aexit__(self, *args):
    pass
  
  @abstractmethod
  async def commit(self):
    pass
  
  @abstractmethod
  async def rollback(self):
    pass