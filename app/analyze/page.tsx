"use client"

import { useState, type FormEvent, type ChangeEvent } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ShieldAlert, Loader2 } from "lucide-react"
import Link from "next/link"
import { ScoreCard } from "@/components/score-card"
import { ExplanationPanel } from "@/components/explanation-panel"

interface AnalysisResult {
  score: number
  label: "safe" | "suspicious" | "high_risk"
  explanation: Array<{ feature: string; contribution: number }>
  model_version: string
  timestamp?: string
  processing_time_ms?: number
}

export default function AnalyzePage() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    price: "",
    seller: "",
    rating: "",
    review_count: "",
    category: "electronics",
    country: "US",
    images: "",
  })
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const payload = {
        ...formData,
        price: Number.parseFloat(formData.price),
        rating: Number.parseFloat(formData.rating),
        review_count: Number.parseInt(formData.review_count),
        images: formData.images ? formData.images.split("\n").filter(Boolean) : [],
      }

      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (!response.ok) throw new Error("Analysis failed")
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError((err as Error).message || "An error occurred")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-background to-blue-50/10">
      <header className="border-b border-border/40 sticky top-0 z-50 backdrop-blur-sm bg-background/80">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center gap-2">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition">
            <ShieldAlert className="w-6 h-6 text-indigo-600" />
            <h1 className="text-xl font-bold text-foreground">FakeDetect AI</h1>
          </Link>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-6 py-12">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-2">Analyze Listing</h2>
          <p className="text-muted-foreground">Submit product details for instant AI fraud detection</p>
        </div>

        <div className="grid gap-8 md:grid-cols-2">
          {/* Form */}
          <Card className="bg-white rounded-2xl shadow-lg p-8 border-0 h-fit sticky top-24">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-1.5">Product Title *</label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                  placeholder="e.g., iPhone 15 Pro Max"
                  className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-1.5">Description</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Product description..."
                  rows={3}
                  className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1.5">Price *</label>
                  <input
                    type="number"
                    name="price"
                    value={formData.price}
                    onChange={handleChange}
                    required
                    step="0.01"
                    placeholder="99.99"
                    className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1.5">Seller *</label>
                  <input
                    type="text"
                    name="seller"
                    value={formData.seller}
                    onChange={handleChange}
                    required
                    placeholder="Seller name"
                    className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1.5">Rating (0-5) *</label>
                  <input
                    type="number"
                    name="rating"
                    value={formData.rating}
                    onChange={handleChange}
                    required
                    step="0.1"
                    min="0"
                    max="5"
                    placeholder="4.5"
                    className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1.5">Reviews *</label>
                  <input
                    type="number"
                    name="review_count"
                    value={formData.review_count}
                    onChange={handleChange}
                    required
                    min="0"
                    placeholder="150"
                    className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1.5">Category *</label>
                  <select
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition"
                  >
                    <option>electronics</option>
                    <option>clothing</option>
                    <option>jewelry</option>
                    <option>watches</option>
                    <option>books</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1.5">Country *</label>
                  <select
                    name="country"
                    value={formData.country}
                    onChange={handleChange}
                    className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground focus:outline-none focus:ring-2 focus:ring-primary transition"
                  >
                    <option>US</option>
                    <option>IN</option>
                    <option>CN</option>
                    <option>UK</option>
                    <option>CA</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-1.5">Image URLs</label>
                <textarea
                  name="images"
                  value={formData.images}
                  onChange={handleChange}
                  placeholder="https://example.com/image1.jpg&#10;https://example.com/image2.jpg"
                  rows={2}
                  className="w-full px-4 py-2.5 rounded-lg border border-border bg-white text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary transition text-sm"
                />
              </div>

              <Button
                type="submit"
                disabled={loading}
                className="w-full mt-6 bg-primary hover:bg-primary/90 text-primary-foreground font-medium py-2.5 rounded-lg transition disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                {loading ? "Analyzing..." : "Analyze Listing"}
              </Button>

              <p className="text-xs text-muted-foreground text-center">* Required fields</p>
            </form>
          </Card>

          {/* Results */}
          <div className="space-y-4">
            {error && (
              <Card className="bg-red-50 border border-red-200 rounded-2xl p-6">
                <p className="text-red-700 font-medium text-sm">⚠️ Error: {error}</p>
              </Card>
            )}

            {result && (
              <div className="space-y-4 animate-fade-in">
                <Card className="bg-white rounded-2xl shadow-lg p-8 border-0">
                  <ScoreCard score={result.score} label={result.label} processingTime={result.processing_time_ms} />
                </Card>

                {result.explanation && result.explanation.length > 0 && (
                  <ExplanationPanel explanations={result.explanation} />
                )}

                <Card className="bg-blue-50 border border-blue-200 rounded-2xl p-4">
                  <p className="text-sm text-blue-800">
                    <strong>Model:</strong> {result.model_version} •<strong className="ml-2">Generated:</strong>{" "}
                    {new Date(result.timestamp || "").toLocaleTimeString()}
                  </p>
                </Card>
              </div>
            )}

            {!result && !error && (
              <Card className="bg-white rounded-2xl shadow-lg p-12 border-0 text-center">
                <div className="space-y-3">
                  <ShieldAlert className="w-12 h-12 mx-auto text-muted-foreground/40" />
                  <p className="text-muted-foreground font-medium">Submit a listing to see analysis results</p>
                  <p className="text-sm text-muted-foreground">Our AI will analyze the product in real-time</p>
                </div>
              </Card>
            )}
          </div>
        </div>

        <div className="mt-12 text-center">
          <Link href="/">
            <Button variant="outline" className="rounded-lg bg-transparent">
              ← Back to Home
            </Button>
          </Link>
        </div>
      </div>
    </main>
  )
}
