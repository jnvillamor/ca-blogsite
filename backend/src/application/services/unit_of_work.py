from abc import ABC, abstractmethod
from src.application.repositories import (
  IUserRepository
)

class IUnitOfWork(ABC):
  users: IUserRepository
  
  @abstractmethod
  def __enter__(self):
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