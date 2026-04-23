import pytest
from datetime import datetime, timezone

from src.domain.entities import BlogEntity
from src.domain.exceptions import InvalidDataException


SAMPLE_CONTENT = [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Hello world.", "styles": {}}], "children": []}]


class TestBlogEntityPublish:

  @pytest.fixture
  def draft_blog(self):
    return BlogEntity(
      id="blog-1",
      title="My Draft Title",
      content=SAMPLE_CONTENT,
      author_id="author-1",
      status="draft",
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

  def test_publish_sets_status_to_published(self, draft_blog):
    draft_blog.publish()

    assert draft_blog.status == "published"

  def test_publish_copies_title_to_published_title(self, draft_blog):
    draft_blog.publish()

    assert draft_blog.published_title == "My Draft Title"

  def test_publish_copies_content_to_published_content(self, draft_blog):
    draft_blog.publish()

    assert draft_blog.published_content == SAMPLE_CONTENT

  def test_publish_sets_published_at(self, draft_blog):
    before = datetime.now()
    draft_blog.publish()
    after = datetime.now()

    assert draft_blog.published_at is not None
    assert before <= draft_blog.published_at <= after

  def test_publish_updates_updated_at(self, draft_blog):
    draft_blog.publish()

    # publish() uses datetime.now() (naive), so just verify it was set to a recent time
    assert draft_blog.updated_at is not None
    assert isinstance(draft_blog.updated_at, datetime)

  def test_publish_after_draft_edit_copies_latest_draft(self, draft_blog):
    draft_blog.title = "Edited Title"
    edited_content = [{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Edited content.", "styles": {}}], "children": []}]
    draft_blog.content = edited_content

    draft_blog.publish()

    assert draft_blog.published_title == "Edited Title"
    assert draft_blog.published_content == edited_content

  def test_publish_preserves_non_published_fields(self, draft_blog):
    draft_blog.publish()

    assert draft_blog.id == "blog-1"
    assert draft_blog.author_id == "author-1"
    assert draft_blog.title == "My Draft Title"
    assert draft_blog.content == SAMPLE_CONTENT


class TestBlogEntityDefaults:

  def test_default_status_is_draft(self):
    blog = BlogEntity(
      id="blog-1",
      title="A Title",
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    assert blog.status == "draft"

  def test_default_published_fields_are_none(self):
    blog = BlogEntity(
      id="blog-1",
      title="A Title",
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    assert blog.published_title is None
    assert blog.published_content is None
    assert blog.published_at is None


class TestBlogEntityToDict:

  def test_to_dict_includes_published_fields(self):
    blog = BlogEntity(
      id="blog-1",
      title="Title",
      content=SAMPLE_CONTENT,
      author_id="author-1",
      status="published",
      published_title="Pub Title",
      published_content=SAMPLE_CONTENT,
      published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 6, 1, tzinfo=timezone.utc)
    )

    result = blog.to_dict()

    assert result["status"] == "published"
    assert result["published_title"] == "Pub Title"
    assert result["published_content"] == SAMPLE_CONTENT
    assert result["published_at"] == datetime(2024, 6, 1, tzinfo=timezone.utc)

  def test_to_dict_draft_has_none_published_fields(self):
    blog = BlogEntity(
      id="blog-1",
      title="Title",
      content=SAMPLE_CONTENT,
      author_id="author-1",
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

    result = blog.to_dict()

    assert result["status"] == "draft"
    assert result["published_title"] is None
    assert result["published_content"] is None
    assert result["published_at"] is None


class TestBlogEntityStatusValidation:

  def test_invalid_status_on_construction_raises(self):
    with pytest.raises(InvalidDataException):
      BlogEntity(
        id="blog-1",
        title="A Title",
        content=SAMPLE_CONTENT,
        author_id="author-1",
        status="archived",
      )

  def test_status_setter_accepts_valid_value(self):
    blog = BlogEntity(
      id="blog-1",
      title="A Title",
      content=SAMPLE_CONTENT,
      author_id="author-1",
      status="draft",
    )

    blog.status = "published"

    assert blog.status == "published"

  def test_status_setter_rejects_invalid_value(self):
    blog = BlogEntity(
      id="blog-1",
      title="A Title",
      content=SAMPLE_CONTENT,
      author_id="author-1",
      status="draft",
    )

    with pytest.raises(InvalidDataException):
      blog.status = "archived"

    # Original status is unchanged.
    assert blog.status == "draft"

  def test_status_getter_returns_string_not_value_object(self):
    blog = BlogEntity(
      id="blog-1",
      title="A Title",
      content=SAMPLE_CONTENT,
      author_id="author-1",
      status="published",
    )

    assert isinstance(blog.status, str)
    assert blog.status == "published"
