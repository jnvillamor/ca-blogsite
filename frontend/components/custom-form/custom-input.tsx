import { useFieldContext } from "."
import { Label } from "../ui/label"
import { Input } from "../ui/input"
import { Button } from "../ui/button"
import { Eye, EyeOff } from "lucide-react"
import { useState } from "react"

type CustomInputFieldProps = {
  label: string
  type: React.InputHTMLAttributes<HTMLInputElement>["type"]
  placeholder?: string
} & React.InputHTMLAttributes<HTMLInputElement>

export const InputField = ({
  label,
  type,
  placeholder,
  ...props
}: CustomInputFieldProps) => {
  const { name, state, handleChange, handleBlur } = useFieldContext<string>()
  const { errors, isTouched } = state.meta

  return (
    <div className="space-y-2">
      <Label htmlFor={name} className="text-sm font-semibold">
        {label}
      </Label>
      <div className="space-y-1">
        <Input
          id={name}
          name={name}
          type={type}
          placeholder={placeholder}
          value={state.value || ""}
          onChange={(e) => handleChange(e.target.value)}
          onBlur={handleBlur}
          {...props}
        />
        {isTouched && errors.length > 0 && (
          <span className="text-destructive text-sm">
            {errors[0]?.message || `Invalid ${label.toLowerCase()}`}
          </span>
        )}
      </div>
    </div>
  )
}

export const SenstiveInputField = ({
  label,
  placeholder,
  ...props
}: Omit<CustomInputFieldProps, "type">) => {
  const [showPassword, setShowPassword] = useState(false)
  const { name, state, handleChange, handleBlur } = useFieldContext<string>()
  const { errors, isTouched } = state.meta

  return (
    <div className="space-y-2">
      <Label htmlFor={name} className="text-sm font-semibold">
        {label}
      </Label>
      <div className="space-y-1">
        <div className="relative">
          <Input
            id={name}
            name={name}
            type={showPassword ? "text" : "password"}
            placeholder={placeholder}
            value={state.value || ""}
            onChange={(e) => handleChange(e.target.value)}
            onBlur={handleBlur}
            {...props}
          />
          <Button
            variant="ghost"
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground cursor-pointer transition-colors"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? (
              <EyeOff className="h-5 w-5" />
            ) : (
              <Eye className="h-5 w-5" />
            )}
          </Button>
        </div>
        {isTouched && errors.length > 0 && (
          <span className="text-destructive text-sm">
            {errors[0]?.message || `Invalid ${label.toLowerCase()}`}
          </span>
        )}
      </div>
    </div>
  )
}