# Development Guide

## Project Structure

\`\`\`
.
├── app/                          # Next.js app directory
│   ├── page.tsx                  # Landing page
│   ├── analyze/page.tsx          # Analysis form
│   ├── monitor/page.tsx          # Realtime monitoring
│   ├── insights/page.tsx         # Model metrics
│   ├── api/
│   │   └── analyze/route.ts      # ML inference API
│   ├── layout.tsx                # Root layout
│   └── globals.css               # Global styles
│
├── components/                   # React components
│   ├── ui/                       # shadcn components (auto-generated)
│   ├── verdict-badge.tsx         # Verdict display
│   ├── score-card.tsx            # Circular score visualization
│   └── explanation-panel.tsx     # Feature explanations
│
├── hooks/                        # Custom React hooks
│   ├── use-mobile.ts
│   └── use-toast.ts
│
├── lib/                          # Utilities
│   └── utils.ts                  # Tailwind classname merging
│
├── ml/                           # Python ML services
│   ├── features.py               # Feature extraction
│   ├── train.py                  # Model training
│   ├── serve.py                  # FastAPI server
│   ├── producer.py               # Synthetic data producer
│   ├── requirements.txt          # Python dependencies
│   ├── notebooks/
│   │   └── eda_and_training.ipynb # Jupyter notebook
│   ├── models/                   # Trained model artifacts
│   ├── test_features.py          # Feature tests
│   └── test_serve.py             # API tests
│
├── dataset/                      # Sample data
│   └── sample-listings.json      # Example listings
│
├── scripts/                      # Utility scripts
│   └── run-producer.sh           # Producer runner
│
├── .github/
│   └── workflows/
│       └── tests.yml             # CI/CD pipeline
│
├── docker-compose.yml            # Service orchestration
├── Dockerfile                    # Frontend build
├── next.config.mjs               # Next.js config
├── tsconfig.json                 # TypeScript config
├── package.json                  # Node dependencies
│
└── README.md                     # Project documentation
\`\`\`

## Common Tasks

### Adding a New Page

1. Create `app/your-page/page.tsx`:
\`\`\`tsx
export default function YourPage() {
  return <main>Your content</main>
}
\`\`\`

2. Link from navigation (update header components)
3. Add to README if user-facing

### Creating a New Component

1. Create `components/your-component.tsx`
2. Export as named export
3. Document props with JSDoc
4. Use in pages/other components

### Adding an API Route

1. Create `app/api/your-endpoint/route.ts`
2. Implement POST/GET handlers
3. Add type definitions
4. Test with curl or Postman

### Training a New Model

1. Update features in `ml/features.py`
2. Run training: `python ml/train.py`
3. Review metrics in output
4. Model saved to `ml/models/`

### Running the Full Demo

\`\`\`bash
# Terminal 1: Start services
docker-compose up

# Terminal 2: Run producer
bash scripts/run-producer.sh 120

# Terminal 3: Open browser
# http://localhost:3000 - Landing page
# http://localhost:3000/analyze - Test form
# http://localhost:3000/monitor - Watch stream
\`\`\`

## Debugging

### Frontend Debugging
\`\`\`bash
# Enable verbose logging
NEXT_DEBUG=true npm run dev

# Check browser console (F12)
# Use React DevTools browser extension
\`\`\`

### Backend Debugging
\`\`\`python
# Python debugger
import pdb; pdb.set_trace()

# Or use breakpoint() in Python 3.7+
breakpoint()
\`\`\`

### Docker Debugging
\`\`\`bash
# View logs
docker-compose logs -f <service-name>

# Execute command in container
docker-compose exec app npm run build

# SSH into container
docker-compose exec app sh
\`\`\`

## Performance Profiling

### Frontend
\`\`\`bash
npm run build
npm run analyze  # Bundle size analysis
\`\`\`

### Backend
\`\`\`python
# Profile Python code
import cProfile
import pstats

cProfile.run('your_function()', 'output.prof')
pstats.Stats('output.prof').sort_stats('cumulative').print_stats()
\`\`\`

## Database Schema (Optional)

\`\`\`sql
CREATE TABLE listings (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2),
  seller VARCHAR(100),
  rating FLOAT,
  review_count INTEGER,
  category VARCHAR(50),
  country VARCHAR(10),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE analyses (
  id SERIAL PRIMARY KEY,
  listing_id INTEGER REFERENCES listings(id),
  score FLOAT,
  label VARCHAR(20),
  features JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_listings_seller ON listings(seller);
CREATE INDEX idx_analyses_created ON analyses(created_at);
\`\`\`

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [FastAPI](https://fastapi.tiangolo.com)
- [scikit-learn](https://scikit-learn.org)
\`\`\`
