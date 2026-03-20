"use client"

import { useAppForm } from "@/components/custom-form"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { registerUser } from "@/data-access/auth/auth.data-access"
import { RegisterData, RegisterSchema } from "@/data-access/types/auth.types"
import { signIn } from "next-auth/react"
import { useRouter } from "next/navigation"
import { toast } from "sonner"

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
          <form.AppField
            name="first_name"
            children={(field) => (
              <field.InputField label="First Name" type="text" />
            )}
          />
          <form.AppField
            name="last_name"
            children={(field) => (
              <field.InputField label="Last Name" type="text" />
            )}
          />
          <form.AppField
            name="username"
            children={(field) => (
              <field.InputField label="Username" type="text" />
            )}
          />
          <form.AppField
            name="password"
            children={(field) => (
              <field.SensitiveInputField
                label="Password"
                placeholder="********"
              />
            )}
          />
          <form.AppField
            name="confirm_password"
            children={(field) => (
              <field.SensitiveInputField
                label="Confirm Password"
                placeholder="********"
              />
            )}
          />

          <form.AppForm>
            <form.SubscribeButton
              label={{ default: "Sign Up", submitting: "Signing Up..." }}
            />
          </form.AppForm>
        </form>
      </CardContent>
    </Card>
  )
}

export default RegisterForm
