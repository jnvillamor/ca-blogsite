from src.application.services import IUnitOfWork
from app.repositories import UserRepository, BlogRepository
from sqlalchemy.ext.asyncio import AsyncSession 

class UnitOfWork(IUnitOfWork):
  def __init__(self, session: AsyncSession):
    self.session = session
    self.users = UserRepository(session)
    self.blogs = BlogRepository(session)
  
  async def __aenter__(self) -> 'IUnitOfWork':
    return self
  
  async def __aexit__(self, *args):
    exc_type, exc_val, exc_tb = args
    if exc_type is not None:
      await self.session.rollback()
    else:
      await self.session.commit()
    await self.session.close()
    
  async def commit(self):
    await self.session.commit()
  
  async def rollback(self):
    await self.session.rollback()
    
# Get unit of work instance
def get_uow(session: AsyncSession) -> UnitOfWork:
  return UnitOfWork(session)
