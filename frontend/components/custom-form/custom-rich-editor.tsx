"use client"

import { BlockNoteEditor, PartialBlock } from "@blocknote/core"
import { useCreateBlockNote } from "@blocknote/react"
import { BlockNoteView } from "@blocknote/mantine"
import "@blocknote/mantine/style.css"
import "@blocknote/core/fonts/inter.css"
import "@/styles/blocknote.css"
import { useFieldContext } from "@/hooks/form"

type ContentType = PartialBlock[]

const RichTextEditor = () => {
  const { name, state, handleChange } = useFieldContext<ContentType>()

  const editor: BlockNoteEditor = useCreateBlockNote({
    initialContent: state.value ? state.value : undefined,
  })

  return (
    <div className="-mx-13.5">
      <BlockNoteView
        editor={editor}
        onChange={() => handleChange(editor.document)}
      />
    </div>
  )
}

export default RichTextEditor
