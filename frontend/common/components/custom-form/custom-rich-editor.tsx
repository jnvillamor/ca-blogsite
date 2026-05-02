'use client'

import { PartialBlock } from '@blocknote/core'
import { useFieldContext } from '@/common/hooks/form'
import BlockNoteRenderer from '@/common/components/blocknote/blocknote-renderer'

type ContentType = PartialBlock[]

const RichTextEditor = () => {
  const { state, handleChange } = useFieldContext<ContentType>()

  return (
    <BlockNoteRenderer
      initialContent={state.value}
      editable
      onChange={handleChange}
      className="-mx-13.5"
    />
  )
}

export default RichTextEditor
