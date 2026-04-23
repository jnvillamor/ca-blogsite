import { config } from '@/config/config'
import { AuthException } from '@/config/exceptions'
import { authConfig } from '@/lib/auth'
import { getServerSession } from 'next-auth'
import { ProfileResponse, UserIncludeOptions } from './dto/user.dto'

const USER_ENDPOINT = `${config.apiEndpoint}/${config.apiVersion}/users`

export const getUserProfile = async (
  username: string,
  include_options?: UserIncludeOptions,
): Promise<ProfileResponse> => {
  const session = await getServerSession(authConfig)

  if (!session) {
    return {
      error: true,
      status_code: 401,
      error_message: 'User is not authenticated',
    }
  }

  const params = new URLSearchParams()
  if (include_options) {
    Object.entries(include_options).forEach(([key, value]) => {
      if (value) params.append(key, 'true')
    })
  }

  const response = await fetch(
    `${USER_ENDPOINT}/by-username/${username}?${params.toString()}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${session?.access_token}`,
      },
    },
  )

  if (!response.ok) {
    const error_data = await response.json()
    return {
      error: true,
      status_code: response.status,
      error_message: error_data.detail || 'Failed to fetch user profile',
    }
  }

  const response_data = await response.json()

  return {
    data: {
      id: response_data.id,
      first_name: response_data.first_name,
      last_name: response_data.last_name,
      username: response_data.username,
      avatar: response_data.avatar,
      created_at: response_data.created_at,
      updated_at: response_data.updated_at,
      blog_count: response_data.blog_count,
    },
    error: false,
  }
}
