import pytest

from src.domain.value_objects import BlogStatus
from src.domain.exceptions import InvalidDataException


class TestBlogStatus:

  def test_allowed_values_expose_draft_and_published(self):
    assert BlogStatus.DRAFT == "draft"
    assert BlogStatus.PUBLISHED == "published"
    assert BlogStatus.ALLOWED == ("draft", "published")

  @pytest.mark.parametrize(
    "value",
    ["draft", "published"],
  )
  def test_valid_values_are_accepted(self, value: str):
    status = BlogStatus(value)
    assert status.value == value

  @pytest.mark.parametrize(
    "value",
    [
      "",
      "DRAFT",
      "Published",
      "archived",
      "unknown",
      " draft",
      "draft ",
    ],
  )
  def test_invalid_values_raise_invalid_data(self, value: str):
    with pytest.raises(InvalidDataException) as exc:
      BlogStatus(value)

    assert "Invalid blog status" in str(exc.value)
    assert "draft" in str(exc.value)
    assert "published" in str(exc.value)

  def test_non_string_value_raises_invalid_data(self):
    with pytest.raises(InvalidDataException):
      BlogStatus(None)  # type: ignore[arg-type]

  def test_passing_draft_constant_works(self):
    status = BlogStatus(BlogStatus.DRAFT)
    assert status.value == "draft"

  def test_passing_published_constant_works(self):
    status = BlogStatus(BlogStatus.PUBLISHED)
    assert status.value == "published"
