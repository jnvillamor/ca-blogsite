import { useCallback, useRef, useState } from "react"

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

  const last_saved_ref = useRef<string>('')
  const has_seen_first_value = useRef(false)
  const timeout_ref = useRef<NodeJS.Timeout | null>(null)

  const triggerAutosave = useCallback((data: T) => {
      const serialized = JSON.stringify(data)

      if (!has_seen_first_value.current) {
        has_seen_first_value.current = true
        last_saved_ref.current = serialized
        return
      }

      if (serialized === last_saved_ref.current) return

      localStorage.setItem(storageKey, serialized)

      if (timeout_ref.current) clearTimeout(timeout_ref.current)

      timeout_ref.current = setTimeout(async () => {
        try {
          setStatus("saving")
          await onSave(data)
          last_saved_ref.current = serialized
          setStatus("saved")
        } catch (err) {
          setStatus("error")
        }
      }, delay)
    }, [delay, onSave, storageKey],
  )

  return { triggerAutosave, status }
}

export default useAutoSaveForm
