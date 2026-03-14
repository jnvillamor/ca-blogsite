import { z } from "zod"

export const LoginSchema = z.object({
  username: z.string().min(1, "Username is required"),
  password: z.string().min(1, "Password is required"),
})

export type LoginData = z.infer<typeof LoginSchema>

export const RegisterSchema = z
  .object({
    first_name: z.string().min(1, "First name is required"),
    last_name: z.string().min(1, "Last name is required"),
    username: z.string().min(1, "Username is required"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirm_password: z
      .string()
      .min(8, "Confirm password must be at least 8 characters"),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
  })
  .refine((data) => data.password.length >= 8, {
    message: "Password must be at least 8 characters",
    path: ["password"],
  })
  .refine((data) => /[A-Z]/.test(data.password), {
    message: "Password must contain at least one uppercase letter",
    path: ["password"],
  })
  .refine((data) => /[a-z]/.test(data.password), {
    message: "Password must contain at least one lowercase letter",
    path: ["password"],
  })
  .refine((data) => /[0-9]/.test(data.password), {
    message: "Password must contain at least one number",
    path: ["password"],
  })
  .refine((data) => /[!@#$%^&*(),.?":{}|<>]/.test(data.password), {
    message: "Password must contain at least one special character",
    path: ["password"],
  })

  export type RegisterData = z.infer<typeof RegisterSchema>
