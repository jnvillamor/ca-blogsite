import ProfileCard from './_components/profile-card'
import ProfileActionButtons from './_components/profile-action-buttons'
import ProfileBlogsList from './_components/profile-blogs-list'
import ProtectedPage from '@/common/components/protected-page'
import { getUserProfile } from '@/data-access/user.data-acess'
import { notFound } from 'next/navigation'
import { UserIncludeOptions, UserProfileDTO } from '@/data-access/dto/user.dto'

const Profile = ({ user }: { user: UserProfileDTO }) => {

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-16">
        <ProfileCard user={user} />
        <ProfileActionButtons />
        <ProfileBlogsList />
      </div>
    </main>
  )
}

const ProfilePage = async ({
  params,
}: {
  params: Promise<{ username: string }>
}) => {
  const { username } = await params
  const query: UserIncludeOptions = {
    include_blog_count: true,
  }
  const { data, error, status_code, error_message } = await getUserProfile(username, query)

  if (error && status_code === 404) {
    return notFound()
  }

  if (error || !data) {
    throw new Error(error_message || 'Failed to load user profile')
  }

  return (
    <ProtectedPage>
      <Profile user={data} />
    </ProtectedPage>
  )
}

export default ProfilePage
