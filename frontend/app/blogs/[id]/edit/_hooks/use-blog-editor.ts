'use client'

import { useCallback } from 'react'
import { updateBlog } from '@/data-access/blogs.data-access'
import {
  UpdateBlogData,
  UpdateBlogSchema,
} from '@/data-access/schemas/blogs.schema'
import useAutoSaveForm from '@/app/blogs/_hooks/useAutoSaveForm'

type UseBlogEditorOptions = {
  blogId: string
  delay?: number
}

export const useBlogEditor = ({ blogId, delay = 5000 }: UseBlogEditorOptions) => {
  const onSave = useCallback(
    async (form_data: UpdateBlogData) => {
      const serialized = UpdateBlogSchema.parse(form_data)
      const response = await updateBlog(blogId, serialized)
      if (!response.ok) throw new Error(response.error_message)
    },
    [blogId],
  )

  const { triggerAutosave, status, isDirty, flush } = useAutoSaveForm<UpdateBlogData>({
    delay,
    onSave,
    storageKey: `blog_draft_${blogId}`,
  })

  return { triggerAutosave, status, isDirty, flush }
}
