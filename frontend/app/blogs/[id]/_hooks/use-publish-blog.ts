'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { publishBlog } from '@/data-access/blogs.data-access'

type PublishStatus = 'idle' | 'publishing' | 'success' | 'error'

export const usePublishBlog = (id: string) => {
  const router = useRouter()
  const [status, setStatus] = useState<PublishStatus>('idle')
  const [error, setError] = useState<string | null>(null)

  const publish = useCallback(async () => {
    setStatus('publishing')
    setError(null)
    const response = await publishBlog(id)
    if (!response.ok) {
      setError(response.error_message)
      setStatus('error')
      return
    }
    setStatus('success')
    router.refresh()
  }, [id, router])

  return { publish, status, error }
}
