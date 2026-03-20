import React from "react"
import { useFormContext } from "."
import { Button } from "../ui/button"

type SubscribeButtonProps = {
  label: {
    default: string
    submitting: string
  }
} & React.ButtonHTMLAttributes<HTMLButtonElement>

const SubscribeButton = ({ label, ...props }: SubscribeButtonProps) => {
  const { Subscribe } = useFormContext()

  return (
    <Subscribe selector={(state) => [state.isSubmitting]}>
      {([isSubmitting]) => (
        <Button
          type="submit"
          className="w-full h-11 cursor-pointer"
          disabled={isSubmitting}
          {...props}
        >
          {isSubmitting ? label.submitting : label.default}
        </Button>
      )}
    </Subscribe>
  )
}

export default SubscribeButton
