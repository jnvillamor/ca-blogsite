from src.application.services import IIdGenerator
from uuid import uuid4

class UuidGenerator(IIdGenerator):
  def generate(self):
    return str(uuid4())