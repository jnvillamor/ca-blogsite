'use client'

import { useState, useTransition } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'
import { Eye, MoreVertical, Send, Trash2, Undo2 } from 'lucide-react'
import { Button } from '@/common/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu'
import { publishBlog, unpublishBlog } from '@/data-access/blogs.data-access'
import DeleteBlogDialog from './profile-delete-blog-dialog'

type ProfileBlogActionsProps = {
  blogId: string
  status: 'draft' | 'published'
  isOwner?: boolean
}

const ProfileBlogActions = ({
  blogId,
  status,
  isOwner,
}: ProfileBlogActionsProps) => {
  const router = useRouter()
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [isToggling, startToggleTransition] = useTransition()

  const isPublished = status === 'published'

  const handleToggleStatus = () => {
    startToggleTransition(async () => {
      const response = isPublished
        ? await unpublishBlog(blogId)
        : await publishBlog(blogId)
      if (!response.ok) {
        toast.error(response.error_message)
        return
      }
      toast.success(isPublished ? 'Blog unpublished' : 'Blog published')
      router.refresh()
    })
  }

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            aria-label="Open blog actions"
            className="h-8 w-8 cursor-pointer"
          >
            <MoreVertical className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem asChild>
            <Link href={`/blogs/${blogId}`} className="cursor-pointer">
              <Eye className="h-4 w-4" />
              View
            </Link>
          </DropdownMenuItem>
          {isOwner && (
            <DropdownMenuItem
              className="cursor-pointer"
              disabled={isToggling}
              onSelect={(e) => {
                e.preventDefault()
                handleToggleStatus()
              }}
            >
              {isPublished ? (
                <Undo2 className="h-4 w-4" />
              ) : (
                <Send className="h-4 w-4" />
              )}
              {isToggling
                ? isPublished
                  ? 'Unpublishing…'
                  : 'Publishing…'
                : isPublished
                  ? 'Unpublish'
                  : 'Publish'}
            </DropdownMenuItem>
          )}
          {isOwner && (
            <>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                variant="destructive"
                className="cursor-pointer"
                onSelect={(e) => {
                  e.preventDefault()
                  setDeleteOpen(true)
                }}
              >
                <Trash2 className="h-4 w-4" />
                Delete
              </DropdownMenuItem>
            </>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
      {isOwner && (
        <DeleteBlogDialog
          blogId={blogId}
          open={deleteOpen}
          onOpenChange={setDeleteOpen}
        />
      )}
    </>
  )
}

export default ProfileBlogActions
