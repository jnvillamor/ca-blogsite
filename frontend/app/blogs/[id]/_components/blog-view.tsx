'use client'

import { BlogResponseDTO, PublicBlogResponseDTO } from '@/data-access/dto/blogs.dto'
import OwnerActionBar from './owner-action-bar'
import PublicBlogView from './public-blog-view'
import { useBlogViewMode } from '../_hooks/use-blog-view-mode'

type BlogViewProps = {
  blog: BlogResponseDTO | PublicBlogResponseDTO
  isOwner: boolean
}

const BlogView = ({ blog, isOwner }: BlogViewProps) => {
  if (isOwner) {
    return <OwnerBlogView blog={blog as BlogResponseDTO} />
  }

  return (
    <PublicBlogView
      renderKey={`public-${blog.id}`}
      title={blog.title}
      content={blog.content}
      author={blog.author}
      hero_image={blog.hero_image}
      published_at={blog.published_at}
    />
  )
}

const OwnerBlogView = ({ blog }: { blog: BlogResponseDTO }) => {
  const { mode } = useBlogViewMode()

  const isPreview = mode === 'preview'
  const title = isPreview ? blog.title : blog.published_title ?? blog.title
  const content = isPreview ? blog.content : blog.published_content ?? blog.content

  return (
    <>
      <OwnerActionBar blogId={blog.id} status={blog.status} />
      <PublicBlogView
        renderKey={`${blog.id}-${mode}`}
        title={title}
        content={content}
        author={blog.author}
        hero_image={blog.hero_image}
        published_at={blog.published_at}
      />
    </>
  )
}

export default BlogView
