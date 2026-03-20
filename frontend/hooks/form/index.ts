import SubmitButton from "@/components/custom-form/custom-button"
import { InputField, SensitiveInputField } from "@/components/custom-form/custom-input"
import {
  createFormHook,
  createFormHookContexts,
} from "@tanstack/react-form-nextjs"

export const { fieldContext, useFieldContext, formContext, useFormContext } =
  createFormHookContexts()

export const { useAppForm } = createFormHook({
  fieldComponents: {
    InputField,
    SensitiveInputField,
  },
  formComponents: {
    SubmitButton,
  },
  fieldContext,
  formContext,
})
