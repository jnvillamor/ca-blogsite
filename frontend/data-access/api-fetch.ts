import { ApiResult } from './dto/common.dto'

export const apiFetch = async <T>(
  url: string,
  init: RequestInit,
  fallback_error: string,
): Promise<ApiResult<T>> => {
  const response = await fetch(url, init)

  if (!response.ok) {
    let detail = fallback_error
    try {
      const error_data = await response.json()
      if (error_data?.detail) detail = error_data.detail
    } catch {
      // body not JSON; keep fallback
    }
    return {
      ok: false,
      status_code: response.status,
      error_message: detail,
    }
  }

  if (response.status === 204) {
    return { ok: true, data: null as T }
  }

  return { ok: true, data: (await response.json()) as T }
}

export const unauthenticated = <T>(): ApiResult<T> => ({
  ok: false,
  status_code: 401,
  error_message: 'User is not authenticated',
})
