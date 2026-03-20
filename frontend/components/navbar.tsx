"use client"

import Link from "next/link"
import ThemeToggle from "./theme-toggle"
import { signOut, useSession } from "next-auth/react"
import { Button } from "./ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar"
import { LogOut, Plus, User } from "lucide-react"
import { Spinner } from "./ui/spinner"
import { useState } from "react"

const NavBar = () => {
  const { data: session, status } = useSession()
  const [isLoggingOut, setIsLoggingOut] = useState<boolean>(false)

  const handleSignOut = async (event: Event) => {
    event.preventDefault()
    setIsLoggingOut(true)
    await signOut({ redirect: false })
    setIsLoggingOut(false)
  }

  return (
    <nav className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="h-8 w-8 rounded-lg bg-primary text-primary-foreground flex items-center justify-center font-bold group-hover:shadow-lg transition-shadow">
              B
            </div>
            <span className="text-xl font-bold text-primary group-hover:text-accent transition-colors">
              BlogHub
            </span>
          </Link>

          <div className="flex items-center gap-2">
            <ThemeToggle />

            {status === "loading" ? (
              <Spinner />
            ) : session ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="rounded-full" size="icon">
                    <Avatar>
                      <AvatarImage
                        src={session.user.avatar}
                        alt={`${session.user.first_name} ${session.user.last_name}'s avatar`}
                      />
                      <AvatarFallback>
                        {session.user.first_name.charAt(0)}
                        {session.user.last_name.charAt(0)}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <div className="px-2 py-1 5">
                    <p className="text-sm font-semibold text-foreground">
                      {session.user.first_name} {session.user.last_name}
                    </p>
                    <p className="text-xs text-muted-foreground truncate">
                      {session.user.username}
                    </p>
                  </div>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link
                      href="/profile"
                      className="flex items-center gap-2 cursor-pointer"
                    >
                      <User className="h-4 2-4" />
                      Profile
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link
                      href="/blogs/write"
                      className="flex items-center gap-2 cursor-pointer"
                    >
                      <Plus className="h-4 w-4" />
                      Write Blog
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    onSelect={handleSignOut}
                    className="flex items-center gap-2 text-destructive focus:bg-destructive focus:text-white cursor-pointer"
                  >
                    {isLoggingOut ? (
                      <>
                        <Spinner className="h-5 w-5" />
                        <span>Logging out...</span>
                      </>
                    ) : (
                      <>
                        <LogOut className="h-4 w-4" />
                        <span>Log Out </span>
                      </>
                    )}
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <>
                <Button
                  variant="ghost"
                  size="sm"
                  className="hover:bg-primary/10"
                >
                  <Link href="/login">Sign In</Link>
                </Button>
                <Button variant="outline" size="sm" className="hidden sm:flex">
                  <Link href="/register">Sign Up</Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default NavBar
