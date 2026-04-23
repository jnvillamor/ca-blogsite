import { auth } from "@/lib/auth"
import { headers } from "next/headers"
import { redirect } from "next/navigation"

interface ProtectedPageProps {
  children: React.ReactNode
}

const ProtectedPage = async ({ children }: ProtectedPageProps) => {
  const session = await auth()

  if (!session) {
    const headersList = await headers()
    const pathname = headersList.get("x-next-pathname") ?? "/auth"
    const callbackUrl = encodeURIComponent(pathname)
    redirect(`/login?callbackUrl=${callbackUrl}`)
  }

  return <>{children}</>
}

export default ProtectedPage