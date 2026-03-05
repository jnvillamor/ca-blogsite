import random
from faker import Faker

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import engine
from app.database.models import UserModel, BlogModel
from app.services.uuid_generator import UuidGenerator

faker = Faker()
id_generator = UuidGenerator()

async def seed_users(session: AsyncSession, count: int = 10):
  users = []
  for _ in range(count):
    user = UserModel(
      id=id_generator.generate(),
      first_name=faker.first_name(),
      last_name=faker.last_name(),
      username=faker.unique.user_name(),
      password=faker.password(length=12),
    )

    users.append(user)

  session.add_all(users)
  await session.commit()

  return users

async def seed_blogs(session: AsyncSession, users: list[UserModel], count: int = 20):
  blogs = []
  for _ in range(count):
    blog = BlogModel(
      id=id_generator.generate(),
      title=faker.sentence(nb_words=5),
      content="\n\n".join(faker.paragraphs(nb=5)),
      author_id=random.choice(users).id
    )

    blogs.append(blog)
  
  session.add_all(blogs)
  await session.commit()

async def run_seed():
  print("🌱 Seeding database...")
  async with AsyncSession(engine, expire_on_commit=False) as session:
    users = await seed_users(session)
    await seed_blogs(session, users)
  print("✅ Database seeding complete!")

if __name__ == "__main__":
  import asyncio
  asyncio.run(run_seed())