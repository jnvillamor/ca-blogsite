from abc import ABC, abstractmethod
from src.application.repositories import (
  IUserRepository,
  IBlogRepository
)

class IUnitOfWork(ABC):
  users: IUserRepository
  blogs: IBlogRepository
  
  @abstractmethod
  def __enter__(self) -> 'IUnitOfWork':
    pass
  
  @abstractmethod
  def __exit__(self, *args):
    pass
  
  @abstractmethod
  def commit(self):
    pass
  
  @abstractmethod
  def rollback(self):
    pass