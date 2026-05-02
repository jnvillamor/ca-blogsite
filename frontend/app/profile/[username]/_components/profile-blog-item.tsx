import { Card } from '@/common/components/ui/card'
import { BlockNoteContent } from '@/data-access/schemas/blogs.schema'
import { extractContentPreview, formatReadingTime } from '@/lib/content-preview'
import { CalendarDays, Clock } from 'lucide-react'
import { ReactNode } from 'react'

type ProfileBlogItemProps = {
  title: string
  content: BlockNoteContent[] | null
  status: 'draft' | 'published'
  created_at: string
  actions?: ReactNode
}

const ProfileBlogItem = ({
  title,
  content,
  status,
  created_at,
  actions,
}: ProfileBlogItemProps) => {
  const isPublished = status === 'published'

  return (
    <Card className="transition-colors hover:border-foreground/20">
      <div className="flex flex-col gap-3 p-4 sm:p-6">
        <div className="flex items-center justify-between gap-2">
          <span
            className={`px-2.5 py-0.5 rounded-full text-xs font-medium whitespace-nowrap ${
              isPublished
                ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
            }`}
          >
            {isPublished ? 'Published' : 'Draft'}
          </span>
          {actions}
        </div>

        <div className="space-y-1.5">
          <h3 className="text-base sm:text-lg font-semibold leading-snug line-clamp-2">
            {title}
          </h3>
          <p className="text-sm text-muted-foreground line-clamp-2">
            {extractContentPreview(content, 180)}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 pt-3 border-t text-xs text-muted-foreground">
          <span className="flex items-center gap-1.5">
            <CalendarDays className="h-3.5 w-3.5" />
            {new Date(created_at).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
            })}
          </span>
          <span className="flex items-center gap-1.5">
            <Clock className="h-3.5 w-3.5" />
            {formatReadingTime(content)}
          </span>
        </div>
      </div>
    </Card>
  )
}

export default ProfileBlogItem
