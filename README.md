# Fake Product Detector for E-commerce

AI-powered fraud detection system for e-commerce platforms. Detects fake or misleading product listings using machine learning with explainable verdicts.

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker & Docker Compose

### Local Development

\`\`\`bash
# Clone and install
git clone <repo>
cd fake-product-detector
npm install

# Start all services
docker-compose up

# Frontend: http://localhost:3000
# ML API: http://localhost:8000
# Database: localhost:5432
\`\`\`

### Services

- **Frontend** (Next.js): React UI with Tailwind CSS at http://localhost:3000
- **Backend API** (Node.js/Express): REST API for analysis at http://localhost:3000/api
- **ML Service** (Python/FastAPI): Model inference at http://localhost:8000
- **Database** (PostgreSQL): Stores listings and analysis history

## Project Structure

\`\`\`
.
├── app/                    # Next.js app router
│   ├── page.tsx           # Landing page
│   ├── analyze/           # Analysis form page
│   ├── monitor/           # Realtime stream page
│   ├── insights/          # Model insights page
│   └── api/               # API routes
├── ml/                     # Python ML services
│   ├── train.py           # Model training
│   ├── features.py        # Feature extraction
│   ├── serve.py           # FastAPI inference server
│   └── notebooks/         # Jupyter notebooks
├── dataset/               # Sample data
├── docker-compose.yml     # Service orchestration
└── Dockerfile             # Build configuration
\`\`\`

## Features

- **Real-time Analysis**: Paste product listing → get instant verdict
- **Explainability**: See top contributing features for each prediction
- **Realtime Monitor**: Watch incoming listings with live verdict badges
- **Model Insights**: View accuracy, precision/recall, confusion matrix, feature importance
- **Responsive Design**: Mobile-first Tailwind CSS UI
- **Production Ready**: Docker setup, tests, CI/CD ready

## API

### POST /api/analyze

\`\`\`json
{
  "title": "iPhone 15 Pro Max",
  "description": "Latest smartphone",
  "price": 1199.99,
  "seller": "TechMart",
  "rating": 4.8,
  "review_count": 5234,
  "category": "electronics",
  "country": "US",
  "images": ["https://...jpg"]
}
\`\`\`

Response:

\`\`\`json
{
  "score": 0.87,
  "label": "suspicious",
  "explanation": [
    {"feature": "title_tf_idf_suspicious_word", "contribution": 0.4},
    {"feature": "price_vs_median", "contribution": 0.3}
  ],
  "model_version": "v0.1"
}
\`\`\`

## Testing

\`\`\`bash
# Unit tests
npm test              # Frontend tests
python -m pytest ml/  # Backend ML tests
\`\`\`

## Deployment

Push to GitHub and deploy to Vercel:

\`\`\`bash
git push origin main
\`\`\`

## Roadmap

- [ ] SHAP-based explainability
- [ ] Real image quality checks
- [ ] Batch analysis API
- [ ] Advanced analytics dashboard
- [ ] Model retraining workflow
- [ ] Multi-language support

## License

MIT
