# Architecture Overview

## System Design

\`\`\`
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  React + Next.js + Tailwind (Port 3000)                         │
│  ├─ Landing Page (Dashboard)                                     │
│  ├─ Analyze Page (Form + Results)                                │
│  ├─ Monitor Page (Realtime Stream)                               │
│  └─ Insights Page (Model Metrics)                                │
└──────────────────┬──────────────────────────────────────────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
┌────────▼──────────┐  ┌──────▼──────────────┐
│  Backend API      │  │  ML Inference      │
│  (Next.js Route   │  │  Service           │
│   Handlers)       │  │  (FastAPI)         │
│  Port 3000        │  │  Port 8000         │
└────────┬──────────┘  └──────┬──────────────┘
         │                    │
         └────────┬───────────┘
                  │
         ┌────────▼──────────┐
         │   PostgreSQL      │
         │   Database        │
         │   Port 5432       │
         └───────────────────┘
\`\`\`

## Component Breakdown

### Frontend (React + Next.js)
- **Pages**: Landing, Analyze, Monitor, Insights
- **Components**: VerdictBadge, ScoreCard, ExplanationPanel
- **Client-side State**: Form data, analysis results
- **API Integration**: POST /api/analyze

### Backend API (Next.js Route Handlers)
- **POST /api/analyze**: Receives listing, calls ML service, returns verdict
- **Error Handling**: Fallback to mock predictions if ML service unavailable
- **Validation**: Schema validation for incoming requests

### ML Service (FastAPI)
- **POST /infer**: ML model inference with feature extraction
- **GET /health**: Health check for model availability
- **POST /batch-infer**: Batch processing of multiple listings
- **Models**: RandomForest trained on synthetic data

### Data Layer (PostgreSQL)
- Stores listings and analysis history (optional)
- Query optimization for realtime monitoring
- Row-level security for multi-tenant support (future)

## Data Flow

1. **User submits listing** on frontend
2. **Frontend sends POST** to /api/analyze
3. **Backend validates** input and calls ML service
4. **ML service extracts** features and runs model
5. **Results returned** with explanation
6. **Frontend displays** verdict with visualizations

## Feature Extraction Pipeline

\`\`\`
Raw Listing
├─ Text Features
│  ├─ Suspicious words detection
│  ├─ Caps ratio & special characters
│  └─ Length normalization
├─ Price Features
│  ├─ Deviation from median
│  ├─ Suspiciously low/high
│  └─ Category-based ranges
├─ Rating Features
│  ├─ Perfect rating with low reviews
│  ├─ Review/rating anomalies
│  └─ Normalization
├─ Seller Features
│  ├─ Generic name detection
│  ├─ Official keyword indicators
│  └─ Name patterns
└─ Image Features
   ├─ No images
   ├─ Very few images
   └─ Many images
      ↓
Model Inference
      ↓
Prediction + Explanations
\`\`\`

## Deployment Options

### Docker Compose (Development)
- All services in single command
- Hot reload for frontend development
- Synthetic data for testing

### Kubernetes (Production)
- Separate pods for each service
- Auto-scaling for ML service
- Persistent volume for models
- ConfigMaps for configuration

### Vercel + Cloud Functions
- Frontend on Vercel (Next.js)
- Inference on AWS Lambda / Google Cloud Functions
- Database on Supabase / Cloud SQL
\`\`\`
