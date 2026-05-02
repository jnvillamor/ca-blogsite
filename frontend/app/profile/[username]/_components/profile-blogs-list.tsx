'use client'

import { PaginationParamsDTO } from '@/data-access/dto/common.dto'
import { ProfileBlog, useProfileBlogs } from '../_hooks/use-profile-blogs'
import { Card, CardContent } from '@/common/components/ui/card'
import { Button } from '@/common/components/ui/button'
import Link from 'next/link'
import { extractContentPreview, formatReadingTime } from '@/lib/content-preview'
import { Clock, Edit2, Eye, Trash2 } from 'lucide-react'

type ProfileBlogsListProps = {
  user_id: string
  pagination_params?: PaginationParamsDTO
  isOwner?: boolean
}

const ProfileBlogsList = ({
  user_id,
  pagination_params,
  isOwner,
}: ProfileBlogsListProps) => {
  const { status, blogs, error } = useProfileBlogs(
    user_id,
    pagination_params,
    isOwner,
  )

  if (status === 'loading') {
    return <div>Loading blogs...</div>
  }

  if (status === 'error') {
    return <div>Something went wrong: {error}</div>
  }

  return (
    <section>
      {blogs && blogs.total > 0 ? (
        <div className="space-y-4">
          {blogs.items.map((blog) => {
            return (
              <Card key={blog.id} className="overflow-hidden">
                <div className="flex-flex-col sm:flex-row gap-4 p-6">
                  {/* Blog info */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4 mb-2 flex-wrap">
                      <h3 className="text-lg font-semibold truncate">
                        {blog.title}
                      </h3>

                      <div className="flex gap-2 items-center">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap ${
                            blog.published_at
                              ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                              : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
                          }`}
                        >
                          {blog.published_at ? 'Published' : 'Draft'}
                        </span>
                      </div>
                    </div>

                    {/* Content Preview */}
                    <p className="text-sm text-foreground line-clamp-2 mt-2 mb-3">
                      {extractContentPreview(blog.content, 180)}
                    </p>

                    {/* Metadata */}
                    <div className="flex flex-col sm:flex-row gap-3 text-xs text-muted-foreground">
                      <span>
                        Created{' '}
                        {new Date(blog.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'short',
                          day: 'numeric',
                        })}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {formatReadingTime(blog.content)}
                      </span>
                    </div>
                  </div>
                  {/* Blog Actions */}
                  <ProfileBlogsListActions blog={blog} isOwner={isOwner} />
                </div>
              </Card>
            )
          })}
        </div>
      ) : (
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-muted-foreground mb-4">
              {isOwner
                ? "You haven't written any blogs yet."
                : 'This user has not published any blogs yet.'}
            </p>
            {isOwner && (
              <Button asChild>
                <Link href="">Write Your First Blog</Link>
              </Button>
            )}
          </CardContent>
        </Card>
      )}
    </section>
  )
}

const ProfileBlogsListActions = ({
  blog,
  isOwner,
}: {
  blog: ProfileBlog
  isOwner?: boolean
}) => {
  return (
    <div className="flex flex-col sm:flex-row gap-2 sm:items-center sm:justify-end">
      <Button variant="ghost" size="sm" asChild className="gap-2">
        <Link href={`/blogs/${blog.id}`}>
          <Eye className="h-4 w-4" />
          <span className="hidden sm:inline">View</span>
        </Link>
      </Button>
      {isOwner && (
        <>
          <Button variant="ghost" size="sm" asChild className="gap-2">
            <Link href={`/blogs/${blog.id}/edit`}>
              <Edit2 className="h-4 w-4" />
              <span className="hidden sm:inline">Edit</span>
            </Link>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            className="gap-2 text-destructive hover:text-destructive cursor-pointer"
          >
            <Trash2 className="h-4 w-4" />
            <span className="hidden sm:inline">Delete</span>
          </Button>
        </>
      )}
    </div>
  )
}

export default ProfileBlogsList
