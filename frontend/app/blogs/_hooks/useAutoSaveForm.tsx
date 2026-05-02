import { useCallback, useEffect, useRef, useState } from "react"

type AutoSaveOptions<T> = {
  delay?: number
  onSave: (data: T) => Promise<void> | void
  storageKey?: string
}

type AutoSaveStatus = "idle" | "saving" | "saved" | "error"

const useAutoSaveForm = <T,>({
  delay = 1500,
  onSave,
  storageKey = "auto_save_form_data",
}: AutoSaveOptions<T>) => {
  const [status, setStatus] = useState<AutoSaveStatus>("idle")
  const [isDirty, setIsDirty] = useState(false)

  const last_saved_ref = useRef<string>("")
  const pending_data_ref = useRef<{ data: T; serialized: string } | null>(null)
  const has_seen_first_value = useRef(false)
  const timeout_ref = useRef<ReturnType<typeof setTimeout> | null>(null)
  const saving_promise_ref = useRef<Promise<void> | null>(null)
  const on_save_ref = useRef(onSave)

  useEffect(() => {
    on_save_ref.current = onSave
  }, [onSave])

  const performSave = useCallback(async (): Promise<void> => {
    if (timeout_ref.current) {
      clearTimeout(timeout_ref.current)
      timeout_ref.current = null
    }

    if (saving_promise_ref.current) {
      try {
        await saving_promise_ref.current
      } catch {
        // already surfaced via status
      }
    }

    const pending = pending_data_ref.current
    if (!pending || pending.serialized === last_saved_ref.current) {
      pending_data_ref.current = null
      setIsDirty(false)
      return
    }

    const promise = (async () => {
      setStatus("saving")
      try {
        await on_save_ref.current(pending.data)
        last_saved_ref.current = pending.serialized
        if (pending_data_ref.current?.serialized === pending.serialized) {
          pending_data_ref.current = null
          setIsDirty(false)
        }
        setStatus("saved")
      } catch (err) {
        setStatus("error")
        throw err
      }
    })()

    saving_promise_ref.current = promise
    try {
      await promise
    } finally {
      if (saving_promise_ref.current === promise) {
        saving_promise_ref.current = null
      }
    }
  }, [])

  const triggerAutosave = useCallback(
    (data: T) => {
      const serialized = JSON.stringify(data)

      if (!has_seen_first_value.current) {
        has_seen_first_value.current = true
        last_saved_ref.current = serialized
        return
      }

      if (serialized === last_saved_ref.current) {
        pending_data_ref.current = null
        setIsDirty(false)
        if (timeout_ref.current) {
          clearTimeout(timeout_ref.current)
          timeout_ref.current = null
        }
        return
      }

      pending_data_ref.current = { data, serialized }
      setIsDirty(true)
      localStorage.setItem(storageKey, serialized)

      if (timeout_ref.current) clearTimeout(timeout_ref.current)
      timeout_ref.current = setTimeout(() => {
        performSave().catch(() => {
          // status already set to "error"; nothing else to do here
        })
      }, delay)
    },
    [delay, storageKey, performSave],
  )

  const flush = useCallback(async () => {
    await performSave()
  }, [performSave])

  return { triggerAutosave, status, isDirty, flush }
}

export default useAutoSaveForm
