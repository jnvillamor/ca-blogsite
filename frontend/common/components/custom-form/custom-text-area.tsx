import { useFieldContext } from "@/common/hooks/form"
import React from "react"
import { Textarea } from "../ui/textarea"

const CustomTextArea = ({
  className,
  ...props
}: { className?: string | undefined } & React.ComponentProps<"textarea">) => {
  const { name, state, handleChange } = useFieldContext<string>()

  return (
    <Textarea
      id={name}
      name={name}
      value={state.value}
      onChange={(e) => handleChange(e.target.value)}
      className={className}
      {...props}
    />
  )
}

export default CustomTextArea
