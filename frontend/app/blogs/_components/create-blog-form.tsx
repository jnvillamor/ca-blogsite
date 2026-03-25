"use client"

import { Separator } from "@/components/ui/separator"
import { useAppForm } from "@/hooks/form"

const CreateBlogForm = () => {
  const form = useAppForm({
    defaultValues: {
      title: "",
      content: "",
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        form.handleSubmit()
      }}
      className="space-y-6"
    >
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
        <p className="text-foreground/50">@username</p>
      </div>

      <Separator />

      <div className="min-h-125">
        <form.AppField
          name="content"
          children={(field) => <field.RichTextEditor />}
        />
      </div>
    </form>
  )
}

export default CreateBlogForm
