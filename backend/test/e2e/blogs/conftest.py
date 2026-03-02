import pytest
from datetime import datetime, timezone
from app.database.models import BlogModel

@pytest.fixture()
def existing_blogs(existing_users, create_existing_users):
  return [
    {
      "id": f"blog-{i+1}",
      "title": f"Test Blog {i+1}",
      "content": f"This is the content of test blog {i+1}.",
      "author_id": existing_users[i % len(existing_users)]["id"],
      "hero_image": f"http://example.com/hero{i+1}.jpg",
      "created_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      "updated_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    }
    for i in range(15)
  ]

@pytest.fixture()
def create_existing_blogs(db_session, existing_blogs):
  blog_models = [BlogModel(**blog) for blog in existing_blogs]
  db_session.add_all(blog_models)
  db_session.commit()

@pytest.fixture()
def api_version():
  return "v1"