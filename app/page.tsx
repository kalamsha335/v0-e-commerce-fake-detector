import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ShieldAlert, Upload, BarChart3, Zap } from "lucide-react"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-background to-blue-50/10">
      {/* Header */}
      <header className="border-b border-border/40 sticky top-0 z-50 backdrop-blur-sm bg-background/80">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-6 h-6 text-indigo-600" />
            <h1 className="text-xl font-bold text-foreground">FakeDetect AI</h1>
          </div>
          <nav className="hidden md:flex gap-6">
            <Link href="/analyze" className="text-sm text-muted-foreground hover:text-foreground transition">
              Analyze
            </Link>
            <Link href="/monitor" className="text-sm text-muted-foreground hover:text-foreground transition">
              Monitor
            </Link>
            <Link href="/insights" className="text-sm text-muted-foreground hover:text-foreground transition">
              Insights
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-bold text-foreground mb-4 text-balance">
            Detect Fake Products in Real Time
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Protect your marketplace with AI-powered fraud detection. Analyze product listings instantly with
            explainable verdicts.
          </p>
        </div>

        {/* CTA Cards */}
        <div className="grid gap-6 md:grid-cols-2 mb-12">
          <Card className="bg-white rounded-2xl shadow-lg p-8 border-0 hover:shadow-xl transition">
            <div className="flex gap-4 mb-4">
              <Upload className="w-6 h-6 text-indigo-600 flex-shrink-0" />
              <div>
                <h3 className="text-xl font-semibold text-foreground mb-2">Analyze Listing</h3>
                <p className="text-muted-foreground">Paste product details and get instant AI verdict</p>
              </div>
            </div>
            <Link href="/analyze">
              <Button className="mt-4 w-full bg-indigo-600 hover:bg-indigo-700">Get Started</Button>
            </Link>
          </Card>

          <Card className="bg-white rounded-2xl shadow-lg p-8 border-0 hover:shadow-xl transition">
            <div className="flex gap-4 mb-4">
              <Zap className="w-6 h-6 text-amber-500 flex-shrink-0" />
              <div>
                <h3 className="text-xl font-semibold text-foreground mb-2">Live Monitor</h3>
                <p className="text-muted-foreground">Watch incoming listings in realtime</p>
              </div>
            </div>
            <Link href="/monitor">
              <Button className="mt-4 w-full bg-amber-500 hover:bg-amber-600">View Stream</Button>
            </Link>
          </Card>
        </div>

        {/* Features Grid */}
        <div className="grid gap-6 md:grid-cols-3 mt-16">
          <Card className="bg-white rounded-2xl shadow-md p-6 border-0">
            <BarChart3 className="w-8 h-8 text-indigo-600 mb-3" />
            <h4 className="font-semibold text-foreground mb-2">Explainable AI</h4>
            <p className="text-sm text-muted-foreground">See exactly which features triggered the fraud flag</p>
          </Card>
          <Card className="bg-white rounded-2xl shadow-md p-6 border-0">
            <ShieldAlert className="w-8 h-8 text-green-600 mb-3" />
            <h4 className="font-semibold text-foreground mb-2">High Accuracy</h4>
            <p className="text-sm text-muted-foreground">ML models trained on real marketplace data</p>
          </Card>
          <Card className="bg-white rounded-2xl shadow-md p-6 border-0">
            <Zap className="w-8 h-8 text-blue-600 mb-3" />
            <h4 className="font-semibold text-foreground mb-2">Lightning Fast</h4>
            <p className="text-sm text-muted-foreground">Results in under 2 seconds, sub-second for batch</p>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/40 mt-20 py-8">
        <div className="max-w-6xl mx-auto px-6 flex justify-between items-center text-sm text-muted-foreground">
          <p>&copy; 2025 FakeDetect AI. All rights reserved.</p>
          <div className="flex gap-4">
            <Link href="#" className="hover:text-foreground transition">
              Docs
            </Link>
            <Link href="#" className="hover:text-foreground transition">
              GitHub
            </Link>
            <Link href="#" className="hover:text-foreground transition">
              API
            </Link>
          </div>
        </div>
      </footer>
    </main>
  )
}
