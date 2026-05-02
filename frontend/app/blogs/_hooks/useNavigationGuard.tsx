'use client'

import { useEffect, useRef } from 'react'

type NavigationGuardOptions = {
  when: boolean
  onAttemptedNavigation: (href: string) => void
}

const useNavigationGuard = ({
  when,
  onAttemptedNavigation,
}: NavigationGuardOptions) => {
  const callback_ref = useRef(onAttemptedNavigation)

  useEffect(() => {
    callback_ref.current = onAttemptedNavigation
  }, [onAttemptedNavigation])

  useEffect(() => {
    if (!when) return

    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault()
    }

    const handleClick = (e: MouseEvent) => {
      if (e.defaultPrevented) return
      if (e.button !== 0) return
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return

      const target = e.target
      if (!(target instanceof Element)) return
      const anchor = target.closest('a')
      if (!anchor) return
      if (anchor.target === '_blank') return

      const href = anchor.getAttribute('href')
      if (!href) return
      if (
        href.startsWith('http://') ||
        href.startsWith('https://') ||
        href.startsWith('#') ||
        href.startsWith('mailto:') ||
        href.startsWith('tel:')
      ) {
        return
      }

      e.preventDefault()
      e.stopPropagation()
      callback_ref.current(href)
    }

    window.addEventListener('beforeunload', handleBeforeUnload)
    document.addEventListener('click', handleClick, true)
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload)
      document.removeEventListener('click', handleClick, true)
    }
  }, [when])
}

export default useNavigationGuard
