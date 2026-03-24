import SubmitButton from "@/components/custom-form/custom-button"
import { InputField, SensitiveInputField } from "@/components/custom-form/custom-input"
import CustomTextArea from "@/components/custom-form/custom-text-area"
import {
  createFormHook,
  createFormHookContexts,
} from "@tanstack/react-form-nextjs"
import dynamic from "next/dynamic"

const RichTextEditor = dynamic(() => import("@/components/custom-form/custom-rich-editor"), { ssr: false })

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
