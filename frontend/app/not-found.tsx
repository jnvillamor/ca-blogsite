import { Button } from '@/common/components/ui/button'
import Link from 'next/link'
import { Home, BookOpen } from 'lucide-react'

export const metadata = {
  title: '404 - Page Not Found',
  description: 'The page you are looking for does not exist.',
}

export default function NotFound() {
  return (
    <>
      <main className="min-h-screen bg-background flex items-center justify-center">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center space-y-8">
            {/* 404 Display */}
            <div className="space-y-4">
              <div className="text-6xl sm:text-7xl lg:text-8xl font-bold text-primary/20">
                404
              </div>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight">
                Page Not Found
              </h1>
              <p className="text-lg text-muted-foreground max-w-xl mx-auto">
                Oops! The page you&apos;re looking for doesn&apos;t exist. It might have been moved or deleted.
              </p>
            </div>

            {/* Illustration - Simple decorative text */}
            <div className="py-8">
              <div className="text-6xl opacity-50">📚</div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <Button asChild size="lg" className="gap-2">
                <Link href="/">
                  <Home className="h-5 w-5" />
                  Back to Home
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="gap-2">
                <Link href="/blogs">
                  <BookOpen className="h-5 w-5" />
                  Browse Blogs
                </Link>
              </Button>
            </div>

            {/* Additional help text */}
            <div className="pt-8 border-t border-border">
              <p className="text-sm text-muted-foreground">
                Need help? Try searching for a blog or{' '}
                <Link href="/" className="text-primary hover:underline">
                  return to the homepage
                </Link>
              </p>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
