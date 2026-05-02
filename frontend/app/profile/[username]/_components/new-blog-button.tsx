'use client'

import { useTransition } from 'react'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'
import { Button } from '@/common/components/ui/button'
import { Spinner } from '@/common/components/ui/spinner'
import { createBlog } from '@/data-access/blogs.data-access'
import { cn } from '@/lib/utils'

type NewBlogButtonProps = {
  children: React.ReactNode
  className?: string
}

const NewBlogButton = ({ children, className }: NewBlogButtonProps) => {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()

  const handleClick = () => {
    startTransition(async () => {
      const response = await createBlog({ title: '', content: [] })
      if (!response.ok) {
        toast.error(response.error_message)
        return
      }
      router.push(`/blogs/${response.data.id}/edit`)
    })
  }

  return (
    <Button
      type="button"
      onClick={handleClick}
      disabled={isPending}
      className={cn('cursor-pointer', className)}
    >
      {isPending ? <Spinner /> : null}
      {children}
    </Button>
  )
}

export default NewBlogButton
