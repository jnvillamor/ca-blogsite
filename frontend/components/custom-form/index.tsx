import {
  createFormHook,
  createFormHookContexts,
} from "@tanstack/react-form-nextjs"
import { InputField, SensitiveInputField,  } from "./custom-input"
import SubscribeButton from "./custom-button"

export const { fieldContext, useFieldContext, formContext, useFormContext } =
  createFormHookContexts()

export const { useAppForm } = createFormHook({
  fieldComponents: {
    InputField,
    SensitiveInputField,
  },
  formComponents: {
    SubscribeButton,
  },
  fieldContext,
  formContext,
})
