import z from "zod"

const BlockNoteContent = z.object({
  type: z.string(),
  content: z.array(z.object({
    type: z.string(),
    text: z.string().optional(),
  })).optional(),
  props: z.record(z.any()).optional(),
})

export type BlockNoteContent = z.infer<typeof BlockNoteContent>

const BlockNoteSchema: z.ZodType<any> = z.lazy(() =>
  z.object({
    id: z.string(),
    type: z.string(),
    props: z.record(z.any()).optional(),
    content: z.array(BlockNoteContent).optional(),
    children: z.array(BlockNoteSchema).optional(),
  }),
)

export const CreateBlogSchema = z.object({
  title: z.string(),
  content: z.array(BlockNoteSchema),
  hero_image: z.string().url().optional(),
})

export type CreateBlogData = z.infer<typeof CreateBlogSchema>
