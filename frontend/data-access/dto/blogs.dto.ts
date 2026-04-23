import { BasicUserDTO } from "./user.dto";

export interface BlogResponseDTO {
  id: string;
  title: string;
  content: Record<string, any>;
  author_id: string;
  status: "draft" | "published";
  published_title?: string;
  published_content?: Record<string, any>; 
  published_at?: string;
  created_at: string;
  updated_at: string;
  hero_image?: string;
  author: BasicUserDTO;
}