import { Button } from '@/common/components/ui/button'
import Link from 'next/link'
import { Eye, Trash2 } from 'lucide-react'

type ProfileBlogActionsProps = {
  blogId: string
  isOwner?: boolean
}

const ProfileBlogActions = ({ blogId, isOwner }: ProfileBlogActionsProps) => {
  return (
    <div className="flex flex-col sm:flex-row gap-2 sm:items-center sm:justify-end">
      <Button variant="ghost" size="sm" asChild className="gap-2">
        <Link href={`/blogs/${blogId}`}>
          <Eye className="h-4 w-4" />
          <span className="hidden sm:inline">View</span>
        </Link>
      </Button>
      {isOwner && (
        <Button
          variant="ghost"
          size="sm"
          className="gap-2 text-destructive hover:text-destructive cursor-pointer"
        >
          <Trash2 className="h-4 w-4" />
          <span className="hidden sm:inline">Delete</span>
        </Button>
      )}
    </div>
  )
}

export default ProfileBlogActions
