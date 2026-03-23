import React from "react"
import { Button, buttonVariants } from "../ui/button"
import { useFormContext } from "@/hooks/form"
import { cn } from "@/lib/utils"
import { VariantProps } from "class-variance-authority"

type SubscribeButtonProps = {
  className?: string
  variant?: string
  label: {
    default: string
    submitting: string
  }
} & React.ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof buttonVariants>

const SubmitButton = ({
  label,
  className,
  variant = "default",
  ...props
}: SubscribeButtonProps) => {
  const { Subscribe } = useFormContext()

  return (
    <Subscribe selector={(state) => [state.isSubmitting, state.canSubmit]}>
      {([isSubmitting, canSubmit]) => (
        <Button
          type="submit"
          className={cn("w-full cursor-pointer", className)}
          disabled={isSubmitting || !canSubmit}
          variant={variant}
          {...props}
        >
          {isSubmitting ? label.submitting : label.default}
        </Button>
      )}
    </Subscribe>
  )
}

export default SubmitButton
