import React from "react"
import { Button } from "../ui/button"
import { useFormContext } from "@/hooks/form"

type SubscribeButtonProps = {
  label: {
    default: string
    submitting: string
  }
} & React.ButtonHTMLAttributes<HTMLButtonElement>

const SubmitButton = ({ label, ...props }: SubscribeButtonProps) => {
  const { Subscribe } = useFormContext()

  return (
    <Subscribe selector={(state) => [state.isSubmitting, state.canSubmit]}>
      {([isSubmitting, canSubmit]) => (
        <Button
          type="submit"
          className="w-full h-11 cursor-pointer"
          disabled={isSubmitting || !canSubmit}
          {...props}
        >
          {isSubmitting ? label.submitting : label.default}
        </Button>
      )}
    </Subscribe>
  )
}

export default SubmitButton
