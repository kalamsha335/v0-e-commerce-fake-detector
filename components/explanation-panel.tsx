"use client"

import { Card } from "@/components/ui/card"

interface Explanation {
  feature: string
  contribution: number
}

interface ExplanationPanelProps {
  explanations: Explanation[]
}

export function ExplanationPanel({ explanations }: ExplanationPanelProps) {
  // Format feature name for display
  const formatFeatureName = (feature: string): string => {
    return feature
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ")
  }

  const totalContribution = explanations.reduce((sum, e) => sum + e.contribution, 0) || 1

  return (
    <Card className="bg-white rounded-2xl shadow-lg p-6 border-0 space-y-4">
      <div>
        <h3 className="font-semibold text-foreground mb-1">What triggered this verdict?</h3>
        <p className="text-sm text-muted-foreground">Top contributing factors to the fraud score</p>
      </div>

      <div className="space-y-4">
        {explanations.length === 0 ? (
          <p className="text-sm text-muted-foreground text-center py-8">No significant factors detected</p>
        ) : (
          explanations.map((exp, idx) => (
            <div key={idx} className="space-y-1.5 animate-fade-in" style={{ animationDelay: `${idx * 50}ms` }}>
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <p className="text-sm font-medium text-foreground">
                    {idx + 1}. {formatFeatureName(exp.feature)}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5">Impact: {(exp.contribution * 100).toFixed(1)}%</p>
                </div>
              </div>

              {/* Contribution bar */}
              <div className="h-2 rounded-full bg-gray-100 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-full"
                  style={{
                    width: `${(exp.contribution / (totalContribution / explanations.length)) * 100}%`,
                    transition: "width 0.5s ease",
                  }}
                />
              </div>
            </div>
          ))
        )}
      </div>

      <div className="pt-4 border-t border-border text-xs text-muted-foreground">
        <p className="leading-relaxed">
          💡 <strong>How to read this:</strong> Each factor above contributes to the final fraud score. Higher
          percentages mean greater impact. Even low-impact factors combined can indicate fraud.
        </p>
      </div>
    </Card>
  )
}
