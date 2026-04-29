'use server'

import { config } from '@/config/config'
import { BlogResponseDTO } from './dto/blogs.dto'
import { CreateBlogData } from './schemas/blogs.schema'
import { getServerSession } from 'next-auth'
import { authConfig } from '@/lib/auth'
import { AuthException } from '@/config/exceptions'
import { PaginatedResponseDTO, PaginationParamsDTO } from './dto/common.dto'

const BLOGS_URL = `${config.apiEndpoint}/${config.apiVersion}/blogs`

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
 * Fetch blogs by author with optional pagination and public_only filter.
 *
 * @param public_only If true, only fetch published blogs (no auth required).
 */
export const getBlogsByAuthor = async (
  author_id: string,
  pagination_params?: PaginationParamsDTO,
  public_only: boolean = false,
): Promise<PaginatedResponseDTO<BlogResponseDTO>> => {
  const headers: HeadersInit = { 'Content-Type': 'application/json' }
  let path = `${BLOGS_URL}/author/${author_id}`

  if (public_only) {
    path += '/public'
  } else {
    const session = await requireSession()
    headers.Authorization = `Bearer ${session.access_token}`
  }

  const response = await fetch(`${path}?${toQueryString(pagination_params)}`, {
    method: 'GET',
    headers,
  })

  if (!response.ok) {
    const error_data = await response.json()
    throw new Error(error_data.detail || 'Failed to fetch blogs')
  }

  return (await response.json()) as PaginatedResponseDTO<BlogResponseDTO>
}
