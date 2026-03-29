"use client"

import { Separator } from "@/components/ui/separator"
import { useAppForm } from "@/hooks/form"
import useAutoSaveForm from "../_hooks/useAutoSaveForm"
import { CreateBlogData } from "@/data-access/schemas/blogs.schema"

const CreateBlogForm = () => {
  const local_storage_key = "create_blog_form_data"
  const local_data = localStorage.getItem(local_storage_key)
  console.log(local_data)

  const form = useAppForm({
    defaultValues: local_data ? JSON.parse(local_data) : {
      title: "",
      content: "",
    },
  })

  const { triggerAutosave, status } = useAutoSaveForm<CreateBlogData>({
    delay: 5000,
    onSave: async (form_data: CreateBlogData) => {
      console.log("Auto-saving form data:", form_data)
    },
    storageKey: "create_blog_form_data",
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

      <form.Subscribe selector={(state) => state.values}>
        {(values) => {
          triggerAutosave(values)
          return null
        }}
      </form.Subscribe>
    </form>
  )
}

export default CreateBlogForm
