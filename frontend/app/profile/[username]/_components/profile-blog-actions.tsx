'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Eye, MoreVertical, Trash2 } from 'lucide-react'
import { Button } from '@/common/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu'
import DeleteBlogDialog from './profile-delete-blog-dialog'

type ProfileBlogActionsProps = {
  blogId: string
  isOwner?: boolean
}

const ProfileBlogActions = ({ blogId, isOwner }: ProfileBlogActionsProps) => {
  const [deleteOpen, setDeleteOpen] = useState(false)

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
