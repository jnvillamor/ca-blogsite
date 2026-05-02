import { Card } from '@/common/components/ui/card'
import { Skeleton } from '@/common/components/ui/skeleton'

type ProfileBlogsListSkeletonProps = {
  count?: number
}

const ProfileBlogsListSkeleton = ({
  count = 3,
}: ProfileBlogsListSkeletonProps) => {
  return (
    <section className="space-y-4" aria-busy="true" aria-live="polite">
      {Array.from({ length: count }).map((_, index) => (
        <ProfileBlogItemSkeleton key={index} />
      ))}
    </section>
  )
}

const ProfileBlogItemSkeleton = () => (
  <Card className="transition-colors">
    <div className="flex flex-col gap-3 p-4 sm:p-6">
      <div className="flex items-center justify-between gap-2">
        <Skeleton className="h-5 w-20 rounded-full" />
        <Skeleton className="h-8 w-8 rounded-md" />
      </div>

      <div className="space-y-2">
        <Skeleton className="h-5 sm:h-6 w-3/4" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 pt-3 border-t">
        <Skeleton className="h-3.5 w-24" />
        <Skeleton className="h-3.5 w-20" />
      </div>
    </div>
  </Card>
)

export default ProfileBlogsListSkeleton
