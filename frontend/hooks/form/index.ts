import SubmitButton from "@/components/custom-form/custom-button"
import { InputField, SensitiveInputField } from "@/components/custom-form/custom-input"
import RichTextEditor from "@/components/custom-form/custom-rich-editor"
import CustomTextArea from "@/components/custom-form/custom-text-area"
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
    CustomTextArea,
    RichTextEditor,
  },
  formComponents: {
    SubmitButton,
  },
  fieldContext,
  formContext,
})
