import React from "react"
import RegisterForm from "./_components/RegisterForm"

const Register = () => {
  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center space-y-2">
          <h2 className="text-3xl font-bold text-foreground">Join BlogHub</h2>
          <p className="text-muted-foreground">
            Create your account to start sharing your stories
          </p>
        </div>
        <RegisterForm />
      </div>
    </div>
  )
}

export default Register
