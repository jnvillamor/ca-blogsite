import { Card } from '@/common/components/ui/card'
import { BlockNoteContent } from '@/data-access/schemas/blogs.schema'
import { extractContentPreview, formatReadingTime } from '@/lib/content-preview'
import { Clock } from 'lucide-react'
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
    <Card className="overflow-hidden">
      <div className="flex flex-col sm:flex-row gap-4 p-6">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold truncate mb-2">{title}</h3>

          <p className="text-sm text-foreground line-clamp-2 mt-2 mb-3">
            {extractContentPreview(content, 180)}
          </p>

          <div className="flex flex-col sm:flex-row gap-3 text-xs text-muted-foreground">
            <span>
              Created{' '}
              {new Date(created_at).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
              })}
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {formatReadingTime(content)}
            </span>
          </div>
        </div>

        <div className="flex flex-col items-end gap-2 shrink-0">
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap ${
              isPublished
                ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
            }`}
          >
            {isPublished ? 'Published' : 'Draft'}
          </span>
          {actions}
        </div>
      </div>
    </Card>
  )
}

export default ProfileBlogItem
