"use client"

import { Separator } from "@/components/ui/separator"
import {
  CreateBlogSchema,
  CreateBlogData,
} from "@/data-access/schemas/blogs.schema"
import { useAppForm } from "@/hooks/form"

const CreateBlogForm = () => {
  const form = useAppForm({
    defaultValues: {
      title: "",
      content: "",
    },
    validators: {
      onSubmit: () => CreateBlogSchema,
    },
    onSubmit: async ({ value }: { value: CreateBlogData }) => {
      try {
        const blogData = CreateBlogSchema.parse(value)
        console.log(blogData)
      } catch (error) {
        console.error("Blog creation failed:", error)
      }
    },
  })

  return (
    <div className="flex flex-col px-8 md:py-10 w-full">
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
    </div>
  )
}

export default CreateBlogForm
