import { notFound, redirect } from 'next/navigation'
import { getServerSession } from 'next-auth'
import { authConfig } from '@/lib/auth'
import { getMyBlogById } from '@/data-access/blogs.data-access'
import EditBlogForm from './_components/edit-blog-form'

const EditBlogPage = async ({
  params,
}: {
  params: Promise<{ id: string }>
}) => {
  const { id } = await params
  const session = await getServerSession(authConfig)

  if (!session) {
    redirect(`/login?callbackUrl=/blogs/${id}/edit`)
  }

  const result = await getMyBlogById(id)

  if (!result.ok) {
    if (result.status_code === 404 || result.status_code === 403) {
      return notFound()
    }
    throw new Error(result.error_message)
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <EditBlogForm blog={result.data} username={session.user.username} />
      </div>
    </main>
  )
}

export default EditBlogPage
