'use server'

import { config } from '@/config/config'
import { BlogResponseDTO, PublicBlogResponseDTO } from './dto/blogs.dto'
import { CreateBlogData } from './schemas/blogs.schema'
import { getServerSession } from 'next-auth'
import { authConfig } from '@/lib/auth'
import { AuthException } from '@/config/exceptions'
import { PaginatedResponseDTO, PaginationParamsDTO } from './dto/common.dto'

const BLOGS_URL = `${config.apiEndpoint}/${config.apiVersion}/blogs`
const ME_BLOGS_URL = `${config.apiEndpoint}/${config.apiVersion}/users/me/blogs`

const toQueryString = (params?: PaginationParamsDTO) => {
  const search = new URLSearchParams()
  for (const [key, value] of Object.entries(params ?? {})) {
    if (value !== undefined && value !== null) search.append(key, String(value))
  }
  return search.toString()
}

const requireSession = async () => {
  const session = await getServerSession(authConfig)
  if (!session) throw new AuthException('User is not authenticated')
  return session
}

export const createBlog = async (
  data: CreateBlogData,
): Promise<BlogResponseDTO> => {
  const session = await requireSession()

  const response = await fetch(BLOGS_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify({ ...data, author_id: session.user.id }),
  })

  if (!response.ok) {
    const error_data = await response.json()
    throw new Error(error_data.detail || 'Failed to create blog')
  }

  return (await response.json()) as BlogResponseDTO
}

/**
 * Fetch published blogs for a given author. Public endpoint, no auth required.
 * Returns the published snapshot (title/content) via PublicBlogResponseDTO.
 */
export const getPublicBlogsByAuthor = async (
  author_id: string,
  pagination_params?: PaginationParamsDTO,
): Promise<PaginatedResponseDTO<PublicBlogResponseDTO>> => {
  const path = `${BLOGS_URL}/author/${author_id}`

  const response = await fetch(`${path}?${toQueryString(pagination_params)}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  })

  if (!response.ok) {
    const error_data = await response.json()
    throw new Error(error_data.detail || 'Failed to fetch blogs')
  }

  return (await response.json()) as PaginatedResponseDTO<PublicBlogResponseDTO>
}

/**
 * Fetch ALL blogs (drafts + published) owned by the authenticated user.
 * Author is derived from the JWT on the backend.
 */
export const getMyBlogs = async (
  pagination_params?: PaginationParamsDTO,
): Promise<PaginatedResponseDTO<BlogResponseDTO>> => {
  const session = await requireSession()

  const response = await fetch(
    `${ME_BLOGS_URL}?${toQueryString(pagination_params)}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${session.access_token}`,
      },
    },
  )

  if (!response.ok) {
    const error_data = await response.json()
    throw new Error(error_data.detail || 'Failed to fetch blogs')
  }

  return (await response.json()) as PaginatedResponseDTO<BlogResponseDTO>
}
