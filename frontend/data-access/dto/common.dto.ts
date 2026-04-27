
export interface PaginationParamsDTO { 
  skip?: number;
  limit?: number;
  search?: string;
}

export interface PaginatedResponseDTO<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}