"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { ShieldAlert, Activity } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

interface Listing {
  id: string
  title: string
  seller: string
  score: number
  label: "safe" | "suspicious" | "high_risk"
  timestamp: string
}

export default function MonitorPage() {
  const [listings, setListings] = useState<Listing[]>([])
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    // Simulate realtime data stream
    const interval = setInterval(() => {
      const newListing: Listing = {
        id: Math.random().toString(),
        title: `Product ${Math.floor(Math.random() * 1000)}`,
        seller: `Seller ${Math.floor(Math.random() * 100)}`,
        score: Math.random(),
        label: Math.random() > 0.6 ? "safe" : Math.random() > 0.5 ? "suspicious" : "high_risk",
        timestamp: new Date().toISOString(),
      }
      setListings((prev) => [newListing, ...prev].slice(0, 20))
    }, 3000)

    setConnected(true)
    return () => clearInterval(interval)
  }, [])

  const getRiskColor = (label: string) => {
    switch (label) {
      case "safe":
        return "bg-green-100 text-green-800"
      case "suspicious":
        return "bg-amber-100 text-amber-800"
      case "high_risk":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-background via-background to-blue-50/10">
      <header className="border-b border-border/40 backdrop-blur-sm bg-background/80">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center gap-2">
          <ShieldAlert className="w-6 h-6 text-indigo-600" />
          <h1 className="text-xl font-bold text-foreground">FakeDetect AI</h1>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-2">Live Monitor</h2>
            <p className="text-muted-foreground">Realtime product analysis stream</p>
          </div>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${connected ? "bg-green-500" : "bg-gray-400"}`} />
            <span className="text-sm text-muted-foreground">{connected ? "Connected" : "Disconnected"}</span>
          </div>
        </div>

        <Card className="bg-white rounded-2xl shadow-lg border-0 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-border">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Title</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Seller</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Score</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Verdict</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {listings.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center text-muted-foreground">
                      <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
                      <p>Waiting for incoming listings...</p>
                    </td>
                  </tr>
                ) : (
                  listings.map((listing) => (
                    <tr key={listing.id} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4 text-sm text-foreground truncate">{listing.title}</td>
                      <td className="px-6 py-4 text-sm text-muted-foreground">{listing.seller}</td>
                      <td className="px-6 py-4 text-sm font-medium text-foreground">
                        {(listing.score * 100).toFixed(0)}%
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-block px-3 py-1 rounded-lg text-xs font-medium ${getRiskColor(listing.label)}`}
                        >
                          {listing.label.replace("_", " ")}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-muted-foreground">
                        {new Date(listing.timestamp).toLocaleTimeString()}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </Card>

        <div className="mt-12 text-center">
          <Link href="/">
            <Button variant="outline">Back to Home</Button>
          </Link>
        </div>
      </div>
    </main>
  )
}
