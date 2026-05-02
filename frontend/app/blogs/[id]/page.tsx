import { notFound, redirect } from 'next/navigation'
import { getServerSession } from 'next-auth'
import { authConfig } from '@/lib/auth'
import {
  getBlogById,
  getMyBlogById,
} from '@/data-access/blogs.data-access'
import BlogView from './_components/blog-view'

const BlogPage = async ({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) => {
  const { id } = await params
  const search_params = await searchParams
  const mode = search_params.mode

  const session = await getServerSession(authConfig)

  if (session) {
    const owner_result = await getMyBlogById(id)
    console.log('Owner blog fetch result:', JSON.stringify(owner_result))

    if (owner_result.ok) {
      if (owner_result.data.status === 'draft' && mode !== 'preview') {
        redirect(`/blogs/${id}/edit`)
      }
      return (
        <main className="min-h-screen bg-background">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
            <BlogView blog={owner_result.data} isOwner />
          </div>
        </main>
      )
    }

    if (owner_result.status_code !== 403 && owner_result.status_code !== 404) {
      throw new Error(owner_result.error_message)
    }
    // 403/404 from owner endpoint => not the owner. Fall through to public fetch.
  }

  const public_result = await getBlogById(id)
  if (!public_result.ok) {
    if (public_result.status_code === 404) return notFound()
    throw new Error(public_result.error_message)
  }
  console.log('Public blog fetch result:', public_result)

  return (
    <main className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <BlogView blog={public_result.data} isOwner={false} />
      </div>
    </main>
  )
}

export default BlogPage