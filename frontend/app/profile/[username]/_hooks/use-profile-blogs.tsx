'use client'

import {
  getMyBlogs,
  getPublicBlogsByAuthor,
} from '@/data-access/blogs.data-access'
import { PaginationParamsDTO } from '@/data-access/dto/common.dto'
import { BlockNoteContent } from '@/data-access/schemas/blogs.schema'
import { useEffect, useState } from 'react'

type ProfileBlogsStatus = 'loading' | 'success' | 'error'

export type ProfileBlogItem = {
  id: string
  title: string
  content: BlockNoteContent[] | null
  status: 'draft' | 'published'
  created_at: string
}

type ProfileBlogsResult = {
  items: ProfileBlogItem[]
  total: number
}

export const useProfileBlogs = (
  user_id: string,
  pagination_params?: PaginationParamsDTO,
  isOwner: boolean = false,
) => {
  const [status, setStatus] = useState<ProfileBlogsStatus>('loading')
  const [error, setError] = useState<string | null>(null)
  const [blogs, setBlogs] = useState<ProfileBlogsResult | null>(null)

  useEffect(() => {
    let cancelled = false

    const fetchBlogs = async () => {
      setStatus('loading')
      setError(null)
      try {
        const result: ProfileBlogsResult = isOwner
          ? await fetchOwnerBlogs(pagination_params)
          : await fetchPublicBlogs(user_id, pagination_params)

        if (cancelled) return
        setBlogs(result)
        setStatus('success')
      } catch (err) {
        if (cancelled) return
        console.error('Error fetching blogs for user profile:', err)
        setError(err instanceof Error ? err.message : 'Something went wrong')
        setBlogs(null)
        setStatus('error')
      }
    }

    fetchBlogs()
    return () => {
      cancelled = true
    }
  }, [user_id, pagination_params, isOwner])

  return { status, blogs, error }
}

const fetchOwnerBlogs = async (
  pagination_params?: PaginationParamsDTO,
): Promise<ProfileBlogsResult> => {
  const data = await getMyBlogs(pagination_params)
  const items: ProfileBlogItem[] = data.items.map((blog) => ({
    id: blog.id,
    title: blog.title,
    content: blog.content,
    status: blog.status,
    created_at: blog.created_at,
  }))
  return { items, total: data.total }
}

const fetchPublicBlogs = async (
  user_id: string,
  pagination_params?: PaginationParamsDTO,
): Promise<ProfileBlogsResult> => {
  const data = await getPublicBlogsByAuthor(user_id, pagination_params)
  const items: ProfileBlogItem[] = data.items.map((blog) => ({
    id: blog.id,
    title: blog.title,
    content: blog.content,
    status: blog.status,
    created_at: blog.created_at,
  }))
  return { items, total: data.total }
}
