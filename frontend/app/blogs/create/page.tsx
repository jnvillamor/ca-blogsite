import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"
import CreateBlogForm from "./_components/create-blog-form"
import ProtectedPage from "@/components/protected-page"

const CreateBlog = () => {
  return (
    <div className="min-h-screen bg-background w-full">
      <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
        <Button variant="ghost" className="mb-8">
          <Link href="/profile" className="flex items-center gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Profile
          </Link>
        </Button>

        <div className="flex flex-col px-8 md:py-10 w-full">
          <CreateBlogForm />
        </div>
      </div>
    </div>
  )
}

const CreateBlogPage = () => {
  return (
    <ProtectedPage>
      <CreateBlog />
    </ProtectedPage>
  )
}

export default CreateBlogPage
