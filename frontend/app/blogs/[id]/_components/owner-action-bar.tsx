'use client'

import Link from 'next/link'
import { Button } from '@/common/components/ui/button'
import { Eye, Globe2, Pencil, Send } from 'lucide-react'
import { BlogViewMode, useBlogViewMode } from '../_hooks/use-blog-view-mode'
import { usePublishBlog } from '../_hooks/use-publish-blog'

type OwnerActionBarProps = {
  blogId: string
  status: 'draft' | 'published'
}

const OwnerActionBar = ({ blogId, status }: OwnerActionBarProps) => {
  const { mode, setMode } = useBlogViewMode()
  const { publish, status: publishStatus, error } = usePublishBlog(blogId)

  const isPublished = status === 'published'

  return (
    <div className="sticky top-4 z-20 flex flex-wrap items-center justify-between gap-3 rounded-lg border bg-background/80 backdrop-blur px-4 py-3 mb-6 shadow-sm">
      <div className="flex flex-wrap items-center gap-2">
        <ModeButton
          active={mode === 'preview'}
          onClick={() => setMode('preview')}
          icon={<Eye className="h-4 w-4" />}
          label="Preview Draft"
        />
        {isPublished && (
          <ModeButton
            active={mode === 'published'}
            onClick={() => setMode('published')}
            icon={<Globe2 className="h-4 w-4" />}
            label="View Published"
          />
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {error && (
          <span className="text-xs text-destructive" role="alert">
            {error}
          </span>
        )}
        <Button asChild variant="outline" size="sm" className="gap-2">
          <Link href={`/blogs/${blogId}/edit`}>
            <Pencil className="h-4 w-4" />
            Edit
          </Link>
        </Button>
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

const ModeButton = ({
  active,
  onClick,
  icon,
  label,
}: {
  active: boolean
  onClick: () => void
  icon: React.ReactNode
  label: string
}) => (
  <Button
    variant={active ? 'default' : 'ghost'}
    size="sm"
    className="gap-2"
    onClick={onClick}
  >
    {icon}
    {label}
  </Button>
)

export type { BlogViewMode }
export default OwnerActionBar
