export interface PaginationParamsDTO {
  skip?: number
  limit?: number
  search?: string
}

export interface PaginatedResponseDTO<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

export type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; status_code: number; error_message: string }
