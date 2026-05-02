import { config } from '@/config/config'
import { UserIncludeOptions, UserProfileDTO } from './dto/user.dto'
import { ApiResult } from './dto/common.dto'
import { apiFetch } from './api-fetch'

const USER_ENDPOINT = `${config.apiEndpoint}/${config.apiVersion}/users`

export const getUserProfile = async (
  username: string,
  include_options?: UserIncludeOptions,
): Promise<ApiResult<UserProfileDTO>> => {
  const params = new URLSearchParams()
  if (include_options) {
    Object.entries(include_options).forEach(([key, value]) => {
      if (value) params.append(key, 'true')
    })
  }

  return apiFetch<UserProfileDTO>(
    `${USER_ENDPOINT}/by-username/${username}?${params.toString()}`,
    { method: 'GET', headers: { 'Content-Type': 'application/json' } },
    'Failed to fetch user profile',
  )
}
