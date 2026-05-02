import z from "zod"

const BlockNoteContent = z.object({
  type: z.string(),
  text: z.string().optional(),
  href: z.string().optional(),
  styles: z.record(z.any()).optional(),
  content: z.array(z.any()).optional(),
  props: z.record(z.any()).optional(),
}).passthrough()

export type BlockNoteContent = z.infer<typeof BlockNoteContent>

const BlockNoteSchema: z.ZodType<any> = z.lazy(() =>
  z.object({
    id: z.string(),
    type: z.string(),
    props: z.record(z.any()).optional(),
    content: z.union([z.array(BlockNoteContent), z.string()]).optional(),
    children: z.array(BlockNoteSchema).optional(),
  }).passthrough(),
)

export const CreateBlogSchema = z.object({
  title: z.string(),
  content: z.array(BlockNoteSchema),
  hero_image: z.string().url().optional(),
})

export type CreateBlogData = z.infer<typeof CreateBlogSchema>

export const UpdateBlogSchema = z.object({
  title: z.string().optional(),
  content: z.array(BlockNoteSchema).optional(),
  hero_image: z.string().url().optional(),
})

export type UpdateBlogData = z.infer<typeof UpdateBlogSchema>
