'use client'

import { PaginationParamsDTO } from '@/data-access/dto/common.dto'
import { useProfileBlogs } from '../_hooks/use-profile-blogs'
import { Card, CardContent } from '@/common/components/ui/card'
import { Button } from '@/common/components/ui/button'
import Link from 'next/link'
import ProfileBlogItem from './profile-blog-item'
import ProfileBlogActions from './profile-blog-actions'

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

  if (!blogs || blogs.items.length === 0) {
    return <ProfileBlogsEmptyState isOwner={isOwner} />
  }

  return (
    <section className="space-y-4">
      {blogs.items.map((blog) => (
        <ProfileBlogItem
          key={blog.id}
          title={blog.title}
          content={blog.content}
          status={blog.status}
          created_at={blog.created_at}
          actions={
            <ProfileBlogActions blogId={blog.id} isOwner={isOwner} />
          }
        />
      ))}
    </section>
  )
}

const ProfileBlogsEmptyState = ({ isOwner }: { isOwner?: boolean }) => (
  <Card>
    <CardContent className="py-12 text-center">
      <p className="text-muted-foreground mb-4">
        {isOwner
          ? "You haven't written any blogs yet."
          : 'This user has not published any blogs yet.'}
      </p>
      {isOwner && (
        <Button asChild>
          <Link href="/blogs/new">Write Your First Blog</Link>
        </Button>
      )}
    </CardContent>
  </Card>
)

export default ProfileBlogsList
