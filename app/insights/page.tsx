"use client"

import { Card } from "@/components/ui/card"
import { ShieldAlert, BarChart3 } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function InsightsPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-background to-blue-50/10">
      <header className="border-b border-border/40 backdrop-blur-sm bg-background/80">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center gap-2">
          <ShieldAlert className="w-6 h-6 text-indigo-600" />
          <h1 className="text-xl font-bold text-foreground">FakeDetect AI</h1>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-2 flex items-center gap-2">
            <BarChart3 className="w-8 h-8 text-indigo-600" />
            Model Insights
          </h2>
          <p className="text-muted-foreground">Performance metrics and feature importance</p>
        </div>

        <div className="grid gap-6 md:grid-cols-3 mb-8">
          <Card className="bg-white rounded-2xl shadow-lg p-6 border-0">
            <p className="text-sm text-muted-foreground mb-1">Accuracy</p>
            <p className="text-3xl font-bold text-foreground">94.2%</p>
          </Card>
          <Card className="bg-white rounded-2xl shadow-lg p-6 border-0">
            <p className="text-sm text-muted-foreground mb-1">Precision</p>
            <p className="text-3xl font-bold text-foreground">91.5%</p>
          </Card>
          <Card className="bg-white rounded-2xl shadow-lg p-6 border-0">
            <p className="text-sm text-muted-foreground mb-1">Recall</p>
            <p className="text-3xl font-bold text-foreground">89.8%</p>
          </Card>
        </div>

        <Card className="bg-white rounded-2xl shadow-lg p-8 border-0 mb-8">
          <h3 className="text-xl font-semibold text-foreground mb-6">Top Features</h3>
          <div className="space-y-4">
            {[
              { name: "TF-IDF Suspicious Words", score: 0.28 },
              { name: "Price vs Median Ratio", score: 0.22 },
              { name: "Review/Rating Anomaly", score: 0.18 },
              { name: "Seller History", score: 0.16 },
              { name: "Image Quality Flags", score: 0.12 },
            ].map((feature, idx) => (
              <div key={idx} className="flex justify-between items-center">
                <span className="text-foreground font-medium">{feature.name}</span>
                <div className="flex items-center gap-3">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div className="bg-indigo-600 h-2 rounded-full" style={{ width: `${feature.score * 100}%` }} />
                  </div>
                  <span className="text-sm font-medium text-foreground w-10 text-right">
                    {(feature.score * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <div className="grid gap-6 md:grid-cols-2">
          <Card className="bg-white rounded-2xl shadow-lg p-6 border-0">
            <h3 className="text-lg font-semibold text-foreground mb-4">Confusion Matrix</h3>
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="grid grid-cols-2 gap-4 text-center text-sm">
                <div className="bg-green-100 rounded p-3">
                  <div className="font-bold text-green-800">847</div>
                  <div className="text-green-700 text-xs">True Negative</div>
                </div>
                <div className="bg-red-100 rounded p-3">
                  <div className="font-bold text-red-800">28</div>
                  <div className="text-red-700 text-xs">False Positive</div>
                </div>
                <div className="bg-red-100 rounded p-3">
                  <div className="font-bold text-red-800">42</div>
                  <div className="text-red-700 text-xs">False Negative</div>
                </div>
                <div className="bg-green-100 rounded p-3">
                  <div className="font-bold text-green-800">783</div>
                  <div className="text-green-700 text-xs">True Positive</div>
                </div>
              </div>
            </div>
          </Card>

          <Card className="bg-white rounded-2xl shadow-lg p-6 border-0">
            <h3 className="text-lg font-semibold text-foreground mb-4">Verdict Distribution</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-foreground">Safe</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: "65%" }} />
                  </div>
                  <span className="text-sm font-medium">65%</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-foreground">Suspicious</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div className="bg-amber-500 h-2 rounded-full" style={{ width: "24%" }} />
                  </div>
                  <span className="text-sm font-medium">24%</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-foreground">High Risk</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div className="bg-red-500 h-2 rounded-full" style={{ width: "11%" }} />
                  </div>
                  <span className="text-sm font-medium">11%</span>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <div className="mt-12 text-center">
          <Link href="/">
            <Button variant="outline">Back to Home</Button>
          </Link>
        </div>
      </div>
    </main>
  )
}
