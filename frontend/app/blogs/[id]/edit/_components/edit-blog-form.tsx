'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Separator } from '@/common/components/ui/separator'
import { useAppForm } from '@/common/hooks/form'
import { BlogResponseDTO } from '@/data-access/dto/blogs.dto'
import { useBlogEditor } from '../_hooks/use-blog-editor'
import EditActionBar from './edit-action-bar'
import UnsavedChangesDialog from './unsaved-changes-dialog'
import BlogHero from '../../_components/blog-hero'
import useNavigationGuard from '@/app/blogs/_hooks/useNavigationGuard'

type EditBlogFormProps = {
  blog: BlogResponseDTO
  username: string
}

const EditBlogForm = ({ blog, username }: EditBlogFormProps) => {
  const router = useRouter()
  const {
    triggerAutosave,
    status: autosaveStatus,
    isDirty,
    flush,
  } = useBlogEditor({ blogId: blog.id })

  const [pendingHref, setPendingHref] = useState<string | null>(null)
  const [savingBeforeNav, setSavingBeforeNav] = useState(false)

  useNavigationGuard({
    when: isDirty,
    onAttemptedNavigation: (href) => setPendingHref(href),
  })

  const handleSaveAndContinue = async () => {
    if (!pendingHref) return
    setSavingBeforeNav(true)
    try {
      await flush()
      const href = pendingHref
      setPendingHref(null)
      router.push(href)
    } catch {
      // keep dialog open so user can retry or discard
    } finally {
      setSavingBeforeNav(false)
    }
  }

  const handleDiscard = () => {
    if (!pendingHref) return
    const href = pendingHref
    setPendingHref(null)
    router.push(href)
  }

  const form = useAppForm({
    defaultValues: {
      title: blog.title,
      content: blog.content ?? [],
    },
  })

  return (
    <>
      <EditActionBar
        blogId={blog.id}
        status={blog.status}
        autosaveStatus={autosaveStatus}
        isDirty={isDirty}
        flush={flush}
      />

      <form
        onSubmit={(e) => {
          e.preventDefault()
          form.handleSubmit()
        }}
        className="space-y-6"
      >
        <BlogHero hero_image={blog.hero_image} />

        <div className="space-y-2">
          <form.AppField
            name="title"
            children={(field) => (
              <field.CustomTextArea
                placeholder="Untitled"
                className="focus:outline-none border-none bg-transparent dark:bg-transparent resize-none text-3xl md:text-5xl font-bold overflow-hidden w-full px-0 focus-visible:ring-0"
              />
            )}
          />
          <p className="text-foreground/50">@{username}</p>
        </div>

        <Separator />

        <div className="min-h-125">
          <form.AppField
            name="content"
            children={(field) => <field.RichTextEditor />}
          />
        </div>

        <form.Subscribe selector={(state) => state.values}>
          {(values) => {
            triggerAutosave(values)
            return null
          }}
        </form.Subscribe>
      </form>

      <UnsavedChangesDialog
        open={pendingHref !== null}
        onOpenChange={(open) => {
          if (!open && !savingBeforeNav) setPendingHref(null)
        }}
        onSave={handleSaveAndContinue}
        onDiscard={handleDiscard}
        isSaving={savingBeforeNav}
      />
    </>
  )
}

export default EditBlogForm
