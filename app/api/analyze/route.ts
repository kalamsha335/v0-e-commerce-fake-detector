import { type NextRequest, NextResponse } from "next/server"

interface AnalysisResult {
  score: number
  label: "safe" | "suspicious" | "high_risk"
  explanation: Array<{ feature: string; contribution: number }>
  model_version: string
  timestamp: string
}

async function generateMockAnalysis(data: any): Promise<AnalysisResult> {
  // Generate realistic mock predictions based on input
  let suspiciousness = 0

  // Calculate suspiciousness based on input data
  const title = (data.title || "").toLowerCase()
  const suspiciousWords = ["free", "wow", "amazing", "limited", "urgent", "exclusive", "fake", "replica"]
  const wordMatches = suspiciousWords.filter((w) => title.includes(w)).length
  suspiciousness += wordMatches * 0.15

  // Price anomaly
  const categoryRanges: Record<string, [number, number]> = {
    electronics: [200, 2000],
    clothing: [10, 200],
    jewelry: [50, 5000],
    watches: [100, 10000],
    books: [5, 50],
  }
  const range = categoryRanges[data.category] || [1, 10000]
  const medianPrice = (range[0] + range[1]) / 2
  const priceDeviation = Math.abs(data.price - medianPrice) / medianPrice
  suspiciousness += Math.min(priceDeviation * 0.2, 0.2)

  // Rating anomaly
  if (data.rating >= 4.9 && data.review_count < 10) {
    suspiciousness += 0.15
  }
  if (data.review_count === 0) {
    suspiciousness += 0.1
  }

  // Seller name check
  const seller = (data.seller || "").toLowerCase()
  const genericNames = ["seller", "shop", "store", "mall"]
  if (genericNames.some((n) => seller.includes(n))) {
    suspiciousness += 0.1
  }

  // Image check
  const imageCount = data.images && Array.isArray(data.images) ? data.images.length : 0
  if (imageCount === 0) {
    suspiciousness += 0.1
  }

  // Normalize score to 0-1
  const score = Math.min(suspiciousness, 1)

  // Determine label
  let label: "safe" | "suspicious" | "high_risk"
  if (score < 0.4) {
    label = "safe"
  } else if (score < 0.7) {
    label = "suspicious"
  } else {
    label = "high_risk"
  }

  return {
    score,
    label,
    explanation: [
      { feature: "price_deviation_from_median", contribution: Math.min(priceDeviation * 0.2, 1) },
      { feature: "suspicious_words_in_title", contribution: Math.min(wordMatches * 0.15, 1) },
      { feature: "perfect_rating_low_reviews", contribution: data.rating >= 4.9 && data.review_count < 10 ? 0.15 : 0 },
      { feature: "no_images", contribution: imageCount === 0 ? 0.1 : 0 },
      { feature: "generic_seller_name", contribution: genericNames.some((n) => seller.includes(n)) ? 0.1 : 0 },
    ].filter((e) => e.contribution > 0),
    model_version: "v0.1-mock",
    timestamp: new Date().toISOString(),
  }
}

async function callMLService(data: any): Promise<AnalysisResult> {
  const mlServiceUrl = process.env.ML_SERVICE_URL || "http://localhost:8000"

  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout

    const response = await fetch(`${mlServiceUrl}/infer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
      signal: controller.signal,
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      console.warn(`ML service error: ${response.status}, falling back to mock`)
      return generateMockAnalysis(data)
    }

    const result = await response.json()
    return result
  } catch (error) {
    console.log(
      "[v0] ML service unavailable, using mock analysis:",
      error instanceof Error ? error.message : String(error),
    )
    return generateMockAnalysis(data)
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Validate required fields
    if (
      !body.title ||
      typeof body.price !== "number" ||
      !body.seller ||
      body.rating === undefined ||
      body.review_count === undefined
    ) {
      return NextResponse.json({ error: "Missing or invalid required fields" }, { status: 400 })
    }

    // Call ML service (with automatic fallback)
    const result = await callMLService(body)

    return NextResponse.json(result, { status: 200 })
  } catch (error) {
    console.error("Analysis error:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
