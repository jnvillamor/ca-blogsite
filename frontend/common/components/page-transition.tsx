"use client"

import { usePathname } from "next/navigation"
import React, { useEffect, useState } from "react"

const PageTransitionContainer = ({
  children,
}: {
  children: React.ReactNode
}) => {
  const pathname = usePathname()

  return (
    <main
      key={pathname}
      className="
        animate-in fade-in slide-in-from-bottom-2
        duration-150 ease-in-out
      "
    >
      {children}
    </main>
  )
}

export default PageTransitionContainer
