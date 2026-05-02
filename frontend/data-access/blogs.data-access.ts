'use server'

import { config } from '@/config/config'
import { getServerSession } from 'next-auth'
import { authConfig } from '@/lib/auth'
import { BlogResponseDTO, PublicBlogResponseDTO } from './dto/blogs.dto'
import { CreateBlogData, UpdateBlogData } from './schemas/blogs.schema'
import {
  ApiResult,
  PaginatedResponseDTO,
  PaginationParamsDTO,
} from './dto/common.dto'
import { apiFetch, unauthenticated } from './api-fetch'

const BLOGS_URL = `${config.apiEndpoint}/${config.apiVersion}/blogs`
const ME_BLOGS_URL = `${config.apiEndpoint}/${config.apiVersion}/users/me/blogs`

const jsonHeaders = { 'Content-Type': 'application/json' }

const authHeaders = (token: string) => ({
  ...jsonHeaders,
  Authorization: `Bearer ${token}`,
})

const toQueryString = (params?: PaginationParamsDTO) => {
  const search = new URLSearchParams()
  for (const [key, value] of Object.entries(params ?? {})) {
    if (value !== undefined && value !== null) search.append(key, String(value))
  }
  return search.toString()
}

export const createBlog = async (
  data: CreateBlogData,
): Promise<ApiResult<BlogResponseDTO>> => {
  const session = await getServerSession(authConfig)
  if (!session) return unauthenticated<BlogResponseDTO>()

  return apiFetch<BlogResponseDTO>(
    BLOGS_URL,
    {
      method: 'POST',
      headers: authHeaders(session.access_token),
      body: JSON.stringify({ ...data, author_id: session.user.id }),
    },
    'Failed to create blog',
  )
}

/**
 * Fetch published blogs for a given author. Public endpoint, no auth required.
 */
export const getPublicBlogsByAuthor = async (
  author_id: string,
  pagination_params?: PaginationParamsDTO,
): Promise<ApiResult<PaginatedResponseDTO<PublicBlogResponseDTO>>> =>
  apiFetch<PaginatedResponseDTO<PublicBlogResponseDTO>>(
    `${BLOGS_URL}/author/${author_id}?${toQueryString(pagination_params)}`,
    { method: 'GET', headers: jsonHeaders },
    'Failed to fetch blogs',
  )

/**
 * Fetch ALL blogs (drafts + published) owned by the authenticated user.
 */
export const getMyBlogs = async (
  pagination_params?: PaginationParamsDTO,
): Promise<ApiResult<PaginatedResponseDTO<BlogResponseDTO>>> => {
  const session = await getServerSession(authConfig)
  if (!session) return unauthenticated<PaginatedResponseDTO<BlogResponseDTO>>()

  return apiFetch<PaginatedResponseDTO<BlogResponseDTO>>(
    `${ME_BLOGS_URL}?${toQueryString(pagination_params)}`,
    { method: 'GET', headers: authHeaders(session.access_token) },
    'Failed to fetch blogs',
  )
}

/**
 * Public single-blog fetch. Returns the published snapshot only; 404 if the
 * blog is not published.
 */
export const getBlogById = async (
  id: string,
): Promise<ApiResult<PublicBlogResponseDTO>> =>
  apiFetch<PublicBlogResponseDTO>(
    `${BLOGS_URL}/${id}`,
    { method: 'GET', headers: jsonHeaders },
    'Failed to fetch blog',
  )

/**
 * Owner single-blog fetch. Returns full BlogResponseDTO including draft
 * content + published snapshot.
 */
export const getMyBlogById = async (
  id: string,
): Promise<ApiResult<BlogResponseDTO>> => {
  const session = await getServerSession(authConfig)
  if (!session) return unauthenticated<BlogResponseDTO>()

  return apiFetch<BlogResponseDTO>(
    `${ME_BLOGS_URL}/${id}`,
    { method: 'GET', headers: authHeaders(session.access_token) },
    'Failed to fetch blog',
  )
}

export const updateBlog = async (
  id: string,
  data: UpdateBlogData,
): Promise<ApiResult<BlogResponseDTO>> => {
  const session = await getServerSession(authConfig)
  if (!session) return unauthenticated<BlogResponseDTO>()

  return apiFetch<BlogResponseDTO>(
    `${BLOGS_URL}/${id}`,
    {
      method: 'PUT',
      headers: authHeaders(session.access_token),
      body: JSON.stringify(data),
    },
    'Failed to update blog',
  )
}

export const publishBlog = async (
  id: string,
): Promise<ApiResult<BlogResponseDTO>> => {
  const session = await getServerSession(authConfig)
  if (!session) return unauthenticated<BlogResponseDTO>()

  return apiFetch<BlogResponseDTO>(
    `${BLOGS_URL}/${id}/publish`,
    { method: 'POST', headers: authHeaders(session.access_token) },
    'Failed to publish blog',
  )
}

export const unpublishBlog = async (
  id: string,
): Promise<ApiResult<BlogResponseDTO>> => {
  const session = await getServerSession(authConfig)
  if (!session) return unauthenticated<BlogResponseDTO>()

  return apiFetch<BlogResponseDTO>(
    `${BLOGS_URL}/${id}/unpublish`,
    { method: 'POST', headers: authHeaders(session.access_token) },
    'Failed to unpublish blog',
  )
}

export const deleteBlog = async (id: string): Promise<ApiResult<null>> => {
  const session = await getServerSession(authConfig)
  if (!session) return unauthenticated<null>()

  return apiFetch<null>(
    `${BLOGS_URL}/${id}`,
    { method: 'DELETE', headers: authHeaders(session.access_token) },
    'Failed to delete blog',
  )
}
