# presentation/api/dependencies/user_params.py
from fastapi import Query
from src.application.dto import UserIncludeOptions


def get_user_include_options(
  include_blog_count: bool = Query(
    False, 
    description="Include the user's blog count in the response"
  ),
) -> UserIncludeOptions:
  return UserIncludeOptions(include_blog_count=include_blog_count)