import {
  createFormHook,
  createFormHookContexts,
} from "@tanstack/react-form-nextjs"
import { InputField, SenstiveInputField } from "./custom-input"
import SubscribeButton from "./custom-button"

export const { fieldContext, useFieldContext, formContext, useFormContext } =
  createFormHookContexts()

export const { useAppForm } = createFormHook({
  fieldComponents: {
    InputField,
    SenstiveInputField,
  },
  formComponents: {
    SubscribeButton,
  },
  fieldContext,
  formContext,
})
