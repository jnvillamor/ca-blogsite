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


class TestBlogEntityDraftAcceptsLooseValues:
  """Drafts have a relaxed contract: empty/short title and empty content are
  legal at construction and via setters. Publish-time invariants are tested
  separately in TestBlogEntityPublishInvariants."""

  def test_construction_with_empty_title_does_not_raise(self):
    blog = BlogEntity(
      id="blog-1",
      title="",
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    assert blog.title == ""
    assert blog.status == "draft"

  def test_construction_with_whitespace_only_title_strips_to_empty(self):
    blog = BlogEntity(
      id="blog-1",
      title="   \t  \n",
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    assert blog.title == ""

  def test_construction_with_short_title_does_not_raise(self):
    blog = BlogEntity(
      id="blog-1",
      title="Hi",
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    assert blog.title == "Hi"

  def test_construction_with_long_title_does_not_raise(self):
    long_title = "T" * 200
    blog = BlogEntity(
      id="blog-1",
      title=long_title,
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    assert blog.title == long_title

  def test_construction_with_empty_content_does_not_raise(self):
    blog = BlogEntity(
      id="blog-1",
      title="A Title",
      content=[],
      author_id="author-1"
    )

    assert blog.content == []
    assert blog.status == "draft"

  def test_construction_with_empty_title_and_empty_content_does_not_raise(self):
    """The frontend's 'Write New Blog' flow creates a brand-new draft with
    no title and no content yet."""
    blog = BlogEntity(
      id="blog-1",
      title="",
      content=[],
      author_id="author-1"
    )

    assert blog.title == ""
    assert blog.content == []
    assert blog.status == "draft"

  def test_title_setter_accepts_empty_string(self):
    blog = BlogEntity(
      id="blog-1",
      title="Original Title",
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    blog.title = ""

    assert blog.title == ""

  def test_title_setter_accepts_short_string(self):
    blog = BlogEntity(
      id="blog-1",
      title="Original Title",
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    blog.title = "Hi"

    assert blog.title == "Hi"

  def test_content_setter_accepts_empty_list(self):
    blog = BlogEntity(
      id="blog-1",
      title="A Title",
      content=SAMPLE_CONTENT,
      author_id="author-1"
    )

    blog.content = []

    assert blog.content == []

  def test_construction_with_non_list_content_still_raises(self):
    """The structural type guard on Content is a separate invariant from the
    empty-list check, and still fires at construction time."""
    with pytest.raises(InvalidDataException, match=r"Content must be a JSON array of block objects."):
      BlogEntity(
        id="blog-1",
        title="A Title",
        content="not a list",  # type: ignore[arg-type]
        author_id="author-1"
      )


class TestBlogEntityPublishInvariants:
  """Invariants enforced only at publish time. Each scenario starts from a
  draft that constructs cleanly, then asserts publish() raises."""

  def _make_draft(self, *, title: str = "Valid Draft Title", content=None):
    return BlogEntity(
      id="blog-1",
      title=title,
      content=content if content is not None else SAMPLE_CONTENT,
      author_id="author-1",
      status="draft",
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

  def test_publish_rejects_empty_title(self):
    draft = self._make_draft(title="")

    with pytest.raises(InvalidDataException, match=r"Title cannot be empty."):
      draft.publish()

  def test_publish_rejects_whitespace_only_title(self):
    """Title is stripped on construction, so whitespace-only normalizes to
    empty and triggers the same 'cannot be empty' message."""
    draft = self._make_draft(title="   \t   ")

    with pytest.raises(InvalidDataException, match=r"Title cannot be empty."):
      draft.publish()

  def test_publish_rejects_title_shorter_than_min_length(self):
    draft = self._make_draft(title="Shrt")

    with pytest.raises(InvalidDataException, match=r"Title must be at least 5 characters long."):
      draft.publish()

  def test_publish_rejects_title_longer_than_max_length(self):
    draft = self._make_draft(title="T" * 101)

    with pytest.raises(InvalidDataException, match=r"Title cannot exceed 100 characters."):
      draft.publish()

  def test_publish_rejects_empty_content(self):
    draft = self._make_draft(content=[])

    with pytest.raises(InvalidDataException, match=r"Content cannot be empty."):
      draft.publish()

  def test_publish_failure_does_not_mutate_blog_state(self):
    """If publish() raises, the blog must remain a draft with no published_at
    or snapshot fields set — no half-applied mutation."""
    draft = self._make_draft(title="")

    with pytest.raises(InvalidDataException):
      draft.publish()

    assert draft.status == "draft"
    assert draft.published_title is None
    assert draft.published_content is None
    assert draft.published_at is None

  def test_publish_validates_title_before_content(self):
    """When both fields are invalid, the title error should surface first
    (mirrors the order of the validate_for_publish() calls in publish())."""
    draft = self._make_draft(title="", content=[])

    with pytest.raises(InvalidDataException, match=r"Title cannot be empty."):
      draft.publish()
