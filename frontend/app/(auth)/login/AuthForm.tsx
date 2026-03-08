"use client"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Spinner } from "@/components/ui/spinner"
import { LoginData, LoginSchema } from "@/data-access/types/auth"
import { zodResolver } from "@hookform/resolvers/zod"
import { signIn } from "next-auth/react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useForm } from "react-hook-form"
import { toast } from "sonner"

const AuthForm = () => {
  const router = useRouter()
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginData>({
    resolver: zodResolver(LoginSchema),
  })

  const handleSubmitForm = async (data: LoginData) => {
    const { username, password } = data

    try {
      const res = await signIn("credentials", {
        redirect: false,
        username,
        password,
      })

      if (!res?.ok) {
        toast.error(res?.error || "Login failed")
        return
      }

      toast.success("Logged in successfully")
      router.push("/")
    } catch (error) {
      console.error("Login failed:", error)
    }
  }

  return (
    <Card className="w-full border border-border show-lg">
      <CardHeader className="space-y-2 bg-linear-to-b from-primary/5 to-transparent">
        <CardTitle className="text-3xl font-bold text-foreground">
          Welcome Back
        </CardTitle>
        <CardDescription className="text-base">
          Sign in to your account to access your blogs
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form className="space-y-4" onSubmit={handleSubmit(handleSubmitForm)}>
          <div className="space-y-2.5">
            <Label htmlFor="username" className="text-sm font-semibold">
              Username
            </Label>
            <div>
              <Input {...register("username")} className="h-11" />
              {errors?.username && (
                <p className="text-sm text-red-500">
                  {errors.username.message}
                </p>
              )}
            </div>
          </div>

          <div className="space-y-2.5">
            <Label htmlFor="password" className="text-sm font-semibold">
              Password
            </Label>
            <div>
              <Input
                type="password"
                {...register("password")}
                className="h-11"
              />
              {errors?.password && (
                <p className="text-sm text-red-500">
                  {errors.password.message}
                </p>
              )}
            </div>
          </div>

          <Button
            type="submit"
            disabled={isSubmitting}
            className="w-full h-11 text-base font-semibold transition-all hover:shadow-lg cursor-pointer"
          >
            {isSubmitting ? (
              <>
                <Spinner className="w-5 h-5" />
                <span>Signing in...</span>
              </>
            ) : (
              <span>Sign in</span>
            )}
          </Button>

          <div className="text-center text-sm text-muted-foreground pt-2">
            Don't have an account?{" "}
            <Link
              href="/register"
              className="text-primary font-semibold hover:text-accent transition-colors"
            >
              Sign up
            </Link>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default AuthForm
