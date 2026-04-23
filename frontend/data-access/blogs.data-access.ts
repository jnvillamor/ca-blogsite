"use server"

import { config } from "@/config/config";
import { BlogResponseDTO } from "./dto/blogs.dto";
import { CreateBlogData } from "./schemas/blogs.schema";
import { getServerSession } from "next-auth";
import { authConfig } from "@/lib/auth";
import { AuthException } from "@/config/exceptions";


export const createBlog = async (data: CreateBlogData): Promise<BlogResponseDTO> => {
  const session = await getServerSession(authConfig);

  if (!session) {
    throw new AuthException("User is not authenticated");
  }

  const payload = {
    ...data,
    author_id: session.user.id,
  }

  const response = await fetch(
    `${config.apiEndpoint}/${config.apiVersion}/blogs`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${session.access_token}`,
      },
      body: JSON.stringify(payload),
    }
  )

  if (!response.ok) {
    console.error("Failed to create blog with status:", response.status);
    const error_data = await response.json();
    throw new Error(error_data.detail || "Failed to create blog");
  }

  const response_data = await response.json();
  return response_data as BlogResponseDTO;
}