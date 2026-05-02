import pytest
from datetime import datetime, timezone
from app.database.models import BlogModel

@pytest.fixture()
async def existing_blogs(existing_users, create_existing_users):
  return [
    {
      "id": f"blog-{i+1}",
      "title": f"Test Blog {i+1}",
      "content": [{"id": str(i+1), "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"This is the content of test blog {i+1}.", "styles": {}}], "children": []}],
      "author_id": existing_users[i % len(existing_users)]["id"],
      "hero_image": f"http://example.com/hero{i+1}.jpg",
      # Published-snapshot fields: public endpoints filter on `published_at IS NOT NULL`
      # and the use case swaps in `published_title`/`published_content`. Mirroring the
      # draft fields keeps the existing assertions (title == f"Test Blog {n}", content == ...)
      # working unchanged.
      "status": "published",
      "published_title": f"Test Blog {i+1}",
      "published_content": [{"id": str(i+1), "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"This is the content of test blog {i+1}.", "styles": {}}], "children": []}],
      "published_at": datetime(2024, 6, 1, 0, 0, 0, tzinfo=timezone.utc),
      "created_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      "updated_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    }
    for i in range(15)
  ]

@pytest.fixture()
async def create_existing_blogs(db_session, existing_blogs):
  blog_models = [BlogModel(**blog) for blog in existing_blogs]
  db_session.add_all(blog_models)
  await db_session.commit()

@pytest.fixture()
def api_version():
  return "v1"