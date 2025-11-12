"use client"

import { VerdictBadge } from "./verdict-badge"

interface ScoreCardProps {
  score: number
  label: "safe" | "suspicious" | "high_risk"
  processingTime?: number
}

export function ScoreCard({ score, label, processingTime }: ScoreCardProps) {
  const percentage = score * 100

  const getColor = () => {
    if (label === "safe") return "from-green-400 to-green-600"
    if (label === "suspicious") return "from-amber-400 to-amber-600"
    return "from-red-400 to-red-600"
  }

  return (
    <div className="space-y-6">
      {/* Main Score Circle */}
      <div className="flex flex-col items-center">
        <div className="relative w-32 h-32 mb-6">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
            {/* Background circle */}
            <circle cx="60" cy="60" r="54" fill="none" stroke="#e5e7eb" strokeWidth="8" />
            {/* Progress circle */}
            <circle
              cx="60"
              cy="60"
              r="54"
              fill="none"
              stroke={label === "safe" ? "#16a34a" : label === "suspicious" ? "#d97706" : "#dc2626"}
              strokeWidth="8"
              strokeDasharray={`${(percentage / 100) * 339.29} 339.29`}
              strokeLinecap="round"
              style={{ transition: "stroke-dasharray 0.5s ease" }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className="text-4xl font-bold">{percentage.toFixed(0)}%</div>
            <div className="text-xs text-muted-foreground">Risk Score</div>
          </div>
        </div>

        {/* Verdict Badge */}
        <VerdictBadge label={label} size="lg" />

        {processingTime && (
          <p className="text-xs text-muted-foreground mt-4">Analysis completed in {processingTime.toFixed(0)}ms</p>
        )}
      </div>

      {/* Risk Scale */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>Safe</span>
          <span>Suspicious</span>
          <span>High Risk</span>
        </div>
        <div className="h-2 rounded-full bg-gradient-to-r from-green-500 via-amber-500 to-red-500" />
        <div className="h-1 rounded-full bg-gray-200 relative">
          <div
            className="absolute h-full bg-foreground rounded-full"
            style={{ width: `${percentage}%`, transition: "width 0.5s ease" }}
          />
        </div>
      </div>
    </div>
  )
}
