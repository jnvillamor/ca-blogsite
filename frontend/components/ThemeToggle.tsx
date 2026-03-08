"use client"

import { useTheme } from "next-themes"
import { useEffect, useState } from "react"
import { Button } from "./ui/button"
import { Moon, Sun } from "lucide-react"
import { useSession } from "next-auth/react"

const ThemeToggle = () => {
  const [mounted, setMounted] = useState<boolean>(false)
  const { theme, setTheme } = useTheme()

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <div className="h-10 w-10" />
  }

  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="h-10 w-10 p-0 hover:bg-primary/10 transition-color"
      title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
    >
      {theme === "dark" ? (
        <Sun className="h-5 w-5 text-yellow-500" />
      ) : (
        <Moon className="h-5 w-5 text-slate-600" />
      )}
    </Button>
  )
}

export default ThemeToggle
