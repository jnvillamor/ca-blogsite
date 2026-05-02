'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback } from 'react'

export type BlogViewMode = 'published' | 'preview'

const isValidMode = (value: string | null): value is BlogViewMode =>
  value === 'preview' || value === 'published'

export const useBlogViewMode = (): {
  mode: BlogViewMode
  setMode: (mode: BlogViewMode) => void
} => {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const raw = searchParams.get('mode')
  const mode: BlogViewMode = isValidMode(raw) ? raw : 'published'

  const setMode = useCallback(
    (next: BlogViewMode) => {
      const params = new URLSearchParams(searchParams.toString())
      if (next === 'published') params.delete('mode')
      else params.set('mode', next)
      const query = params.toString()
      router.replace(query ? `${pathname}?${query}` : pathname)
    },
    [router, pathname, searchParams],
  )

  return { mode, setMode }
}
