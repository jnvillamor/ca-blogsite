'use client'

import { BlockNoteEditor, PartialBlock } from '@blocknote/core'
import { useCreateBlockNote } from '@blocknote/react'
import { BlockNoteView } from '@blocknote/mantine'
import { useTheme } from 'next-themes'
import '@blocknote/mantine/style.css'
import '@blocknote/core/fonts/inter.css'
import '@/styles/blocknote.css'

type BlockNoteRendererProps = {
  initialContent?: PartialBlock[] | null
  editable?: boolean
  onChange?: (content: PartialBlock[]) => void
  className?: string
}

const sanitizeInlineContent = (content: unknown): unknown => {
  if (!Array.isArray(content)) return content
  return content.filter((node) => {
    if (!node || typeof node !== 'object') return false
    const n = node as { type?: string; text?: unknown }
    if (n.type === 'text' && typeof n.text !== 'string') return false
    return true
  })
}

const sanitizeBlocks = (
  blocks?: PartialBlock[] | null,
): PartialBlock[] | undefined => {
  if (!blocks) return undefined
  return blocks.map((block) => {
    const next: Record<string, unknown> = { ...block }
    if (Array.isArray(block.content)) {
      next.content = sanitizeInlineContent(block.content)
    }
    if (block.children) {
      next.children = sanitizeBlocks(block.children as PartialBlock[])
    }
    return next as unknown as PartialBlock
  })
}

const BlockNoteRenderer = ({
  initialContent,
  editable = true,
  onChange,
  className,
}: BlockNoteRendererProps) => {
  const sanitized = sanitizeBlocks(initialContent)
  const editor: BlockNoteEditor = useCreateBlockNote({
    initialContent: sanitized && sanitized.length > 0 ? sanitized : undefined,
  })
  const { resolvedTheme } = useTheme()
  const theme = resolvedTheme === 'dark' ? 'dark' : 'light'

  return (
    <div className={className}>
      <BlockNoteView
        editor={editor}
        editable={editable}
        theme={theme}
        onChange={
          editable && onChange ? () => onChange(editor.document) : undefined
        }
      />
    </div>
  )
}

export default BlockNoteRenderer
