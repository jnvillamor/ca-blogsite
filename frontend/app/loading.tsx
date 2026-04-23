"use client";

export default function Loading() {
  return (
    <div className="min-h-screen bg-linear-to-br from-background via-background to-muted flex flex-col items-center justify-center px-4 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-primary/5 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      {/* Content */}
      <div className="relative z-10 text-center space-y-6 max-w-md">
        {/* Logo/Brand */}
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-foreground">BlogHub</h1>
          <p className="text-sm text-muted-foreground">
            Loading your stories...
          </p>
        </div>

        {/* Loading animation - Three dots */}
        <div className="flex items-center justify-center gap-2 h-8">
          <div
            className="w-3 h-3 rounded-full bg-primary animate-bounce"
            style={{ animationDelay: '0s' }}
          />
          <div
            className="w-3 h-3 rounded-full bg-primary animate-bounce"
            style={{ animationDelay: '0.2s' }}
          />
          <div
            className="w-3 h-3 rounded-full bg-primary animate-bounce"
            style={{ animationDelay: '0.4s' }}
          />
        </div>

        {/* Progress text */}
        <div className="space-y-2 pt-4">
          <div className="w-full h-1 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary via-primary to-primary/50 rounded-full"
              style={{
                animation: 'slideInfinite 2s ease-in-out infinite',
              }}
            />
          </div>
          <p className="text-xs text-muted-foreground">Just a moment...</p>
        </div>
      </div>

      {/* Decorative elements */}
      <div className="absolute bottom-0 left-0 right-0 h-1/4 bg-gradient-to-t from-background to-transparent pointer-events-none" />

      <style jsx>{`
        @keyframes slideInfinite {
          0% {
            transform: translateX(-100%);
          }
          50% {
            transform: translateX(100%);
          }
          100% {
            transform: translateX(-100%);
          }
        }

        .delay-1000 {
          animation-delay: 1s;
        }
      `}</style>
    </div>
  )
}
