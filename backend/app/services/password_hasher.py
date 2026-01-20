from src.application.services import IPasswordHasher
import hashlib

class PasswordHasher(IPasswordHasher):
  def hash(self, password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
  
  def verify(self, password, hashed_password):
    return self.hash(password) == hashed_password