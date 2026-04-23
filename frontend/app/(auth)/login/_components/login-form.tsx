"use client"

import { useAppForm } from "@/common/hooks/form"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/common/components/ui/card"
import { LoginData, LoginSchema } from "@/data-access/schemas/auth.schema"
import { signIn } from "next-auth/react"
import { useRouter } from "next/navigation"
import { toast } from "sonner"
import { Label } from "@/common/components/ui/label"

const LoginForm = () => {
  const router = useRouter()
  const form = useAppForm({
    defaultValues: {
      username: "",
      password: "",
    },
    validators: {
      onSubmit: LoginSchema,
      onBlur: LoginSchema,
    },
    onSubmit: async ({ value }: { value: LoginData }) => {
      try {
        const credentials = LoginSchema.parse(value)
        const response = await signIn("credentials", {
          ...credentials,
          redirect: false,
        })

        if (!response?.ok) {
          toast.error(response?.error || "Login failed")
          return
        }

        toast.success("Logged in successfully")
        router.push("/")
      } catch (error) {
        console.error("Login failed:", error)
        toast.error(
          error instanceof Error
            ? error.message
            : "An unexpected error occurred",
        )
      }
    },
  })

  return (
    <Card className="w-full border border-border shadow-lg ">
      <CardHeader className="space-y-2 bg-linear-to-b from-primary/5 to-transparent">
        <CardTitle className="text-3xl font-bold text-foreground">
          Welcome Back
        </CardTitle>
        <CardDescription className="text-base">
          Sign in to your account to access blogs
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form
          onSubmit={(e) => {
            e.preventDefault()
            form.handleSubmit()
          }}
          className="space-y-4"
        >
          <div className="space-y-2">
            <Label
              htmlFor="username"
              className="text-sm font-medium text-foreground"
            >
              Username
            </Label>

            <form.AppField
              name="username"
              children={(field) => (
                <field.InputField
                  type="text"
                  placeholder="Enter your username"
                />
              )}
            />
          </div>

          <div className="space-y-2">
            <Label
              htmlFor="password"
              className="text-sm font-medium text-foreground"
            >
              Password
            </Label>
            <form.AppField
              name="password"
              children={(field) => (
                <field.SensitiveInputField placeholder="********" />
              )}
            />
          </div>

          <form.AppForm>
            <form.SubmitButton
              label={{ default: "Log In", submitting: "Logging In..." }}
            />
          </form.AppForm>
        </form>
      </CardContent>
    </Card>
  )
}

export default LoginForm
