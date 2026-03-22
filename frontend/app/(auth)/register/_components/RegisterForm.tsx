"use client"

import { useAppForm } from "@/hooks/form"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { AuthException } from "@/config/exceptions"
import { registerUser } from "@/data-access/auth/auth.data-access"
import { RegisterData, RegisterSchema } from "@/data-access/schemas/auth.schema"
import { useRouter } from "next/navigation"
import { toast } from "sonner"
import { Label } from "@/components/ui/label"

const RegisterForm = () => {
  const router = useRouter()
  const form = useAppForm({
    defaultValues: {
      first_name: "",
      last_name: "",
      username: "",
      password: "",
      confirm_password: "",
    },
    validators: {
      onSubmit: RegisterSchema,
      onBlur: RegisterSchema,
    },
    onSubmit: async ({ value }: { value: RegisterData }) => {
      try {
        value = RegisterSchema.parse(value)
        await registerUser({
          first_name: value.first_name,
          last_name: value.last_name,
          username: value.username,
          password: value.password,
          confirm_password: value.confirm_password,
        })

        toast.success("Registered successfully")
        router.push("/")
      } catch (error) {
        console.error("Registration failed:", error)
        console.log(error instanceof AuthException)
        toast.error(
          error instanceof AuthException
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
          Create an Account
        </CardTitle>
        <CardDescription className="text-base">
          Join our community and start sharing your stories
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
              htmlFor="first_name"
              className="text-sm font-medium text-foreground"
            >
              First Name
            </Label>
            <form.AppField
              name="first_name"
              children={(field) => (
                <field.InputField
                  type="text"
                  placeholder="Enter your first name"
                />
              )}
            />
          </div>

          <div className="space-y-2">
            <Label
              htmlFor="last_name"
              className="text-sm font-medium text-foreground"
            >
              Last Name
            </Label>

            <form.AppField
              name="last_name"
              children={(field) => (
                <field.InputField
                  type="text"
                  placeholder="Enter your last name"
                />
              )}
            />
          </div>

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

          <div className="space-y-2">
            <Label
              htmlFor="confirm_password"
              className="text-sm font-medium text-foreground"
            >
              Confirm Password
            </Label>

            <form.AppField
              name="confirm_password"
              children={(field) => (
                <field.SensitiveInputField
                  placeholder="********"
                />
              )}
            />
          </div>

          <form.AppForm>
            <form.SubmitButton
              label={{ default: "Sign Up", submitting: "Signing Up..." }}
            />
          </form.AppForm>
        </form>
      </CardContent>
    </Card>
  )
}

export default RegisterForm
