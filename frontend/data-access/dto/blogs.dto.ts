import { BlockNoteContent } from "../schemas/blogs.schema";
import { BasicUserDTO } from "./user.dto";

export interface BlogResponseDTO {
  id: string;
  title: string;
  content: BlockNoteContent[] | null;
  author_id: string;
  status: "draft" | "published";
  published_title?: string;
  published_content?: BlockNoteContent[] | null; 
  published_at?: string;
  created_at: string;
  updated_at: string;
  hero_image?: string;
  author: BasicUserDTO;
}