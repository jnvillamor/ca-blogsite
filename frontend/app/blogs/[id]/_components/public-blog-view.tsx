'use client'

import BlockNoteRenderer from '@/common/components/blocknote/blocknote-renderer'
import { BlockNoteContent } from '@/data-access/schemas/blogs.schema'
import { BasicUserDTO } from '@/data-access/dto/user.dto'
import { Separator } from '@/common/components/ui/separator'
import BlogHero from './blog-hero'

type PublicBlogViewProps = {
  title: string
  content: BlockNoteContent[] | null
  author?: BasicUserDTO
  hero_image?: string
  published_at?: string
  /** Stable identifier for the rendered content. Forces BlockNote to remount when the source changes. */
  renderKey: string
}

const PublicBlogView = ({
  title,
  content,
  author,
  hero_image,
  published_at,
  renderKey,
}: PublicBlogViewProps) => {
  return (
    <article className="space-y-6">
      <BlogHero hero_image={hero_image} />

      <header className="space-y-3">
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight">
          {title}
        </h1>
        <div className="flex flex-wrap items-center gap-x-3 text-sm text-muted-foreground">
          {author && (
            <span>
              By @{author.username}
            </span>
          )}
          {published_at && (
            <>
              <span aria-hidden>·</span>
              <time dateTime={published_at}>
                {new Date(published_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric',
                })}
              </time>
            </>
          )}
        </div>
      </header>

      <Separator />

      <div className="min-h-80">
        <BlockNoteRenderer
          key={renderKey}
          initialContent={content as never}
          editable={false}
          className="-mx-13.5"
        />
      </div>
    </article>
  )
}

export default PublicBlogView
