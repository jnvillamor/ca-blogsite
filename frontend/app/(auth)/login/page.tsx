import AuthForm from "./AuthForm"

export const metadata = {
  title: 'Log In',
  description: 'Log in to your BlogHub account'
}

const LogIn = () => {
  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md px-4 sm:px-6 lg:px-8">
        <div className="mb-8 text-center space-y-2">
          <h2 className="text-3xl font-bold text-foreground">Welcome Back</h2>
          <p className="text-muted-foreground">Access your BlogHub account</p>
        </div>
        <AuthForm />
      </div>
    </div>
  )
}

export default LogIn