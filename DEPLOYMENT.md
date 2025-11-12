# Deployment Guide

## Development Setup

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.11+

### Local Development

\`\`\`bash
# Clone repository
git clone <repo>
cd fake-product-detector

# Start all services
docker-compose up

# Frontend: http://localhost:3000
# ML API: http://localhost:8000
# PostgreSQL: localhost:5432
\`\`\`

### Development Without Docker

\`\`\`bash
# Frontend
npm install
npm run dev  # http://localhost:3000

# ML Service (in another terminal)
cd ml
pip install -r requirements.txt
python -m uvicorn serve:app --reload  # http://localhost:8000

# Database (optional)
docker run -d -p 5432:5432 \
  -e POSTGRES_PASSWORD=dev \
  -e POSTGRES_DB=fakedetect \
  postgres:16-alpine
\`\`\`

## Production Deployment

### Vercel + AWS Lambda

1. **Frontend on Vercel**:
\`\`\`bash
npm run build
# Push to GitHub connected to Vercel
# Auto-deploys on push to main
\`\`\`

2. **ML Service on AWS Lambda**:
\`\`\`bash
# Containerize ML service
docker build -f Dockerfile.ml -t fake-detector-ml .
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag fake-detector-ml:latest <account>.dkr.ecr.us-east-1.amazonaws.com/fake-detector-ml:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/fake-detector-ml:latest

# Create Lambda function from ECR image
# Set environment: MODEL_PATH=/app/models/fake_detector_v0.1.pkl
\`\`\`

3. **Database on Supabase**:
\`\`\`bash
# Create project at supabase.com
# Run migrations
psql postgresql://<user>:<pass>@<host>:<port>/<db> < ml/schema.sql
\`\`\`

### Environment Variables

Create `.env.local` (git-ignored):

\`\`\`env
# Backend
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://yourdomain.com
ML_SERVICE_URL=https://ml-api.yourdomain.com

# ML Service
MODEL_PATH=/app/models/fake_detector_v0.1.pkl
DATABASE_URL=postgresql://user:pass@host/dbname

# Database
POSTGRES_USER=fakedetect
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=fakedetect
\`\`\`

### Monitoring & Logging

\`\`\`bash
# View logs
docker-compose logs -f app

# Health checks
curl http://localhost:8000/health
curl http://localhost:3000/health

# Metrics (optional - add Prometheus)
# curl http://localhost:8000/metrics
\`\`\`

## Scaling Considerations

### Load Balancing
- Use Nginx or AWS ALB in front
- Multiple ML service replicas
- Redis caching for popular listings

### Database Optimization
- Index on (seller, category, country)
- Partitioning by date for analytics
- Archival of old records

### Model Updates
- Version model artifacts in S3/GCS
- Blue-green deployment for new models
- A/B testing framework

## Security

- Enable HTTPS everywhere
- Rate limiting on API endpoints
- Input validation on all endpoints
- RLS policies on database
- Regular dependency updates
- Secrets management (AWS Secrets Manager)
\`\`\`
