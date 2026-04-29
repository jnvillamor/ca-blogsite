import { BlockNoteContent } from '../schemas/blogs.schema'
import { BasicUserDTO } from './user.dto'

export interface PublicBlogResponseDTO {
  id: string
  title: string
  content: BlockNoteContent[] | null
  author_id: string
  status: 'draft' | 'published'
  published_at?: string
  created_at: string
  updated_at: string
  hero_image?: string
  author: BasicUserDTO
}

export interface BlogResponseDTO extends PublicBlogResponseDTO {
  published_title?: string
  published_content?: BlockNoteContent[] | null
}
