import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function Home() {
  return (
    <main className="min-h-screen relative mx-auto px-4 py-50 sm:px-6 lg:px-8 overflow-hidden">
      <div className="absolute inset-0 opacity-15">
        <div className="absolute top-0 right-0 w-100 h-100 bg-primary rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-100 h-100 bg-accent rounded-full blur-3xl"></div>
      </div>

      <div className="text-center space-y-6">
        <div className="space-y-4">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-balance">
            Discover Great{" "}
            <span className="bg-linear-to-r from-primary to-accent bg-clip-text text-transparent">
              Stories
            </span>
          </h1>

          <p className="mx-auto max-w-3xl text-lg sm:text-xl text-muted-foreground text-balance leading-relaxed">
            Explore insightful articles written by our community. Share your
            voice and inspire others with your unique perspective.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-6">
          <Button
            asChild
            size="lg"
            className="h-12 text-base font-semibold shadow-lg hover:shadow-xl transition-shadow"
          >
            <Link href="/register">Start Writing</Link>
          </Button>
          <Button
            asChild
            variant="outline"
            size="lg"
            className="h-12 text-base font-semibold hover:bg-primary/10"
          >
            <Link href="/blogs">Browse Stories</Link>
          </Button>
        </div>
      </div>
    </main>
  )
}
