'use client'

import { Button } from '@/common/components/ui/button'
import Link from 'next/link'
import { AlertCircle, Home, RefreshCw } from 'lucide-react'
import { useEffect } from 'react'

interface ErrorProps {
  error: Error & { digest?: string }
  reset: () => void
}

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('[v0] Error caught by global error boundary:', error)
    }
  }, [error])

  return (
    <>
      <main className="min-h-screen bg-background flex items-center justify-center">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center space-y-8">
            {/* Error Icon */}
            <div className="space-y-4">
              <div className="flex justify-center">
                <div className="p-4 rounded-full bg-destructive/10">
                  <AlertCircle className="h-8 w-8 text-destructive" />
                </div>
              </div>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight">
                Something Went Wrong
              </h1>
              <p className="text-lg text-muted-foreground max-w-xl mx-auto">
                We encountered an unexpected error. Please try again or return to the home page.
              </p>
            </div>

            {/* Error Details - Only in Development */}
            {process.env.NODE_ENV === 'development' && error.message && (
              <div className="rounded-lg border border-destructive/20 bg-destructive/5 p-4">
                <p className="text-sm font-mono text-destructive">
                  <span className="font-semibold">Error:</span> {error.message}
                </p>
                {error.digest && (
                  <p className="text-xs text-muted-foreground mt-2">
                    <span className="font-semibold">Digest:</span> {error.digest}
                  </p>
                )}
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Button
                size="lg"
                className="gap-2"
                onClick={reset}
              >
                <RefreshCw className="h-5 w-5" />
                Try Again
              </Button>
              <Button asChild variant="outline" size="lg" className="gap-2">
                <Link href="/">
                  <Home className="h-5 w-5" />
                  Back to Home
                </Link>
              </Button>
            </div>

            {/* Support Text */}
            <div className="pt-8 border-t border-border">
              <p className="text-sm text-muted-foreground">
                If the problem persists, please refresh the page or{' '}
                <Link href="/" className="text-primary hover:underline">
                  contact support
                </Link>
              </p>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
