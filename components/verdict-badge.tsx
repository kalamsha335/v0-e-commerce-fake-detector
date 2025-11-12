import { CheckCircle, AlertTriangle, AlertCircle } from "lucide-react"

interface VerdictBadgeProps {
  label: "safe" | "suspicious" | "high_risk"
  size?: "sm" | "md" | "lg"
}

export function VerdictBadge({ label, size = "md" }: VerdictBadgeProps) {
  const styles = {
    safe: {
      bg: "bg-green-50",
      text: "text-green-800",
      border: "border-green-200",
      icon: "text-green-600",
    },
    suspicious: {
      bg: "bg-amber-50",
      text: "text-amber-800",
      border: "border-amber-200",
      icon: "text-amber-600",
    },
    high_risk: {
      bg: "bg-red-50",
      text: "text-red-800",
      border: "border-red-200",
      icon: "text-red-600",
    },
  }

  const sizeStyles = {
    sm: "px-2 py-1 text-xs",
    md: "px-3 py-1.5 text-sm",
    lg: "px-4 py-2 text-base",
  }

  const iconSize = {
    sm: "w-3 h-3",
    md: "w-4 h-4",
    lg: "w-5 h-5",
  }

  const style = styles[label]
  const Icon = label === "safe" ? CheckCircle : label === "suspicious" ? AlertTriangle : AlertCircle

  return (
    <div
      className={`inline-flex items-center gap-2 rounded-full border ${style.bg} ${style.border} ${style.text} font-medium ${sizeStyles[size]}`}
    >
      <Icon className={`${iconSize[size]} ${style.icon}`} />
      {label.replace("_", " ")}
    </div>
  )
}
