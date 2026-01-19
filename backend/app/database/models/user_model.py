from app.database.db import Base
from sqlalchemy import Column, String

class UserModel(Base):
  __tablename__ = 'users'
  
  id = Column(String, primary_key=True)
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  username = Column(String, unique=True, nullable=False, index=True)
  password = Column(String, nullable=False)
  avatar = Column(String, nullable=True)
  created_at = Column(String, nullable=False)
  updated_at = Column(String, nullable=False)
  