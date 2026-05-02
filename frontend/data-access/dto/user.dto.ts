export interface BasicUserDTO {
  id: string;
  first_name: string;
  last_name: string;
  username: string;
  avatar?: string
}

export interface BlogCountDTO {
  total_blogs: number;
  published_blogs: number;
  draft_blogs: number;
}

export interface UserIncludeOptions {
  include_blog_count?: boolean;
}

export interface UserProfileDTO extends BasicUserDTO {
  created_at: string;
  updated_at: string;
  blog_count: BlogCountDTO;
}