'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { Button } from '@/common/components/ui/button'
import { Eye, Globe2, Send } from 'lucide-react'
import { usePublishBlog } from '../../_hooks/use-publish-blog'

type AutosaveStatus = 'idle' | 'saving' | 'saved' | 'error'

type EditActionBarProps = {
  blogId: string
  status: 'draft' | 'published'
  autosaveStatus: AutosaveStatus
  isDirty: boolean
  flush: () => Promise<void>
}

const autosaveLabel: Record<AutosaveStatus, string> = {
  idle: '',
  saving: 'Saving…',
  saved: 'Saved',
  error: 'Save failed',
}

const EditActionBar = ({
  blogId,
  status,
  autosaveStatus,
  isDirty,
  flush,
}: EditActionBarProps) => {
  const router = useRouter()
  const [previewing, setPreviewing] = useState(false)
  const { publish, status: publishStatus, error } = usePublishBlog(blogId)
  const isPublished = status === 'published'

  const handlePreview = async () => {
    setPreviewing(true)
    try {
      if (isDirty) {
        await flush()
      }
      router.push(`/blogs/${blogId}?mode=preview`)
    } catch {
      // save failed; autosave status indicator already reflects the error
    } finally {
      setPreviewing(false)
    }
  }

  return (
    <div className="sticky top-4 z-20 flex flex-wrap items-center justify-between gap-3 rounded-lg border bg-background/80 backdrop-blur px-4 py-3 mb-6 shadow-sm">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span
          className={
            autosaveStatus === 'error' ? 'text-destructive' : undefined
          }
          aria-live="polite"
        >
          {autosaveLabel[autosaveStatus]}
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {error && (
          <span className="text-xs text-destructive" role="alert">
            {error}
          </span>
        )}
        <Button
          variant="ghost"
          size="sm"
          className="gap-2"
          onClick={handlePreview}
          disabled={previewing}
        >
          <Eye className="h-4 w-4" />
          {previewing ? 'Saving…' : 'Preview'}
        </Button>
        {isPublished && (
          <Button asChild variant="ghost" size="sm" className="gap-2">
            <Link href={`/blogs/${blogId}?mode=published`}>
              <Globe2 className="h-4 w-4" />
              View Published
            </Link>
          </Button>
        )}
        <Button
          size="sm"
          className="gap-2"
          onClick={publish}
          disabled={publishStatus === 'publishing'}
        >
          <Send className="h-4 w-4" />
          {publishStatus === 'publishing' ? 'Publishing…' : 'Publish'}
        </Button>
      </div>
    </div>
  )
}

export default EditActionBar
