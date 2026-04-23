import z from "zod"

const BlockNoteSchema: z.ZodType<any> = z.lazy(() =>
  z.object({
    id: z.string(),
    type: z.string(),
    props: z.record(z.any()).optional(),
    content: z.any().optional(),
    children: z.array(BlockNoteSchema).optional(),
  }),
)

export const CreateBlogSchema = z.object({
  title: z.string(),
  content: z.array(BlockNoteSchema),
  hero_image: z.string().url().optional(),
})

export type CreateBlogData = z.infer<typeof CreateBlogSchema>
