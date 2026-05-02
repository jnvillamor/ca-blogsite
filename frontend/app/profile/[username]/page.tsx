import ProfileCard from './_components/profile-card'
import ProfileActionButtons from './_components/profile-action-buttons'
import ProfileBlogsList from './_components/profile-blogs-list'
import { getUserProfile } from '@/data-access/user.data-acess'
import { notFound } from 'next/navigation'
import { UserIncludeOptions, UserProfileDTO } from '@/data-access/dto/user.dto'
import { PaginationParamsDTO } from '@/data-access/dto/common.dto'
import { getServerSession, Session } from 'next-auth'
import { authConfig } from '@/lib/auth'

type ProfileProps = {
  user: UserProfileDTO
  pagination_params: PaginationParamsDTO
  isOwner?: boolean
}

const Profile = ({ user, pagination_params, isOwner }: ProfileProps) => {
  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-16">
        <ProfileCard user={user} />
        {isOwner && (
          <ProfileActionButtons />
        )}
        <ProfileBlogsList
          user_id={user.id}
          pagination_params={pagination_params}
          isOwner={isOwner}
        />
      </div>
    </main>
  )
}

const ProfilePage = async ({
  params,
  searchParams,
}: {
  params: Promise<{ username: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) => {
  const session = await getServerSession(authConfig)
  const { username } = await params
  const search_params = await searchParams

  const pagiation_params: PaginationParamsDTO = {
    skip: search_params.skip ? parseInt(search_params.skip as string, 10) : 0,
    limit: search_params.limit
      ? parseInt(search_params.limit as string, 10)
      : 10,
    search: search_params.search as string | undefined,
  }
  const query: UserIncludeOptions = {
    include_blog_count: true,
  }
  const isOwner = session?.user?.username === username

  const result = await getUserProfile(username, query)

  if (!result.ok) {
    if (result.status_code === 404) return notFound()
    throw new Error(result.error_message)
  }

  return <Profile user={result.data} pagination_params={pagiation_params} isOwner={isOwner}/>
}

export default ProfilePage
