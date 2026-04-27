'use client'

import { getBlogsByAuthor } from '@/data-access/blogs.data-access'
import { BlogResponseDTO } from '@/data-access/dto/blogs.dto'
import {
  PaginatedResponseDTO,
  PaginationParamsDTO,
} from '@/data-access/dto/common.dto'
import { useEffect, useState } from 'react'

type UserProfileStatus = 'idle' | 'loading' | 'success' | 'error'

export const useProfileBlogs = (
  user_id: string,
  pagination_params?: PaginationParamsDTO,
) => {
  const [status, setStatus] = useState<UserProfileStatus>('idle')
  const [error, setError] = useState<string | null>(null)
  const [blogs, setBlogs] =
    useState<PaginatedResponseDTO<BlogResponseDTO> | null>(null)

  useEffect(() => {
    const fetchBlogs = async () => {
      setStatus('loading')
      try {
        const blogs_data = await getBlogsByAuthor(user_id, pagination_params)
        console.log(blogs_data)

        setBlogs(blogs_data)
        setStatus('success')
      } catch (error) {
        console.error('Error fetching blogs for user profile:', error)

        setError(
          error instanceof Error ? error.message : 'Something went wrong',
        )
        setBlogs(null)
        setStatus('error')
      } finally {
        setStatus('idle')
      }
    }

    fetchBlogs()
  }, [user_id, pagination_params])

  return { status, blogs, error }
}
