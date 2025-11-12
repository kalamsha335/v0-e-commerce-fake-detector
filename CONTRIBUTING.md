# Contributing Guide

## Development Workflow

1. **Fork & Clone**
\`\`\`bash
git clone https://github.com/yourusername/fake-product-detector.git
cd fake-product-detector
git checkout -b feature/your-feature
\`\`\`

2. **Install & Setup**
\`\`\`bash
npm install
cd ml && pip install -r requirements.txt
docker-compose up
\`\`\`

3. **Make Changes**
- Frontend: Modify files in `app/` and `components/`
- ML: Update files in `ml/`
- Tests: Add unit tests alongside implementations

4. **Test Locally**
\`\`\`bash
npm run lint
npm run build
cd ml && python -m pytest
bash scripts/run-producer.sh 30
\`\`\`

5. **Commit & Push**
\`\`\`bash
git add .
git commit -m "feat: description of your change"
git push origin feature/your-feature
\`\`\`

6. **Create Pull Request**
- Link related issues
- Add description of changes
- Ensure tests pass

## Code Standards

### Frontend (TypeScript + React)
- Use functional components
- Follow ESLint configuration
- Props should be typed
- Add meaningful component names

### Backend (Python)
- Follow PEP 8
- Add docstrings to functions
- Type hints recommended
- Use descriptive variable names

### Commit Messages
\`\`\`
type(scope): subject

Detailed explanation of changes.
- Bullet point 1
- Bullet point 2

Closes #123
\`\`\`

Types: feat, fix, docs, style, refactor, perf, test, ci

## Adding Features

### New ML Feature
1. Add extraction in `ml/features.py`
2. Add test in `ml/test_features.py`
3. Retrain model: `python ml/train.py`
4. Update feature importance documentation

### New UI Page
1. Create page in `app/your-page/page.tsx`
2. Add component in `components/` if reusable
3. Update navigation links
4. Add to README

### New API Endpoint
1. Create route handler in `app/api/your-endpoint/route.ts`
2. Add request/response types
3. Add error handling
4. Document in API section of README

## Testing

### Frontend Tests
\`\`\`bash
npm test
\`\`\`

### Backend Tests
\`\`\`bash
cd ml
python -m pytest test_*.py -v
\`\`\`

### Integration Tests
\`\`\`bash
# Start services
docker-compose up

# Run producer
bash scripts/run-producer.sh 60

# Check results in /monitor
\`\`\`

## Performance Tips

- Use memoization for expensive computations
- Profile with `cProfile` for Python
- Check bundle size: `npm run analyze`
- Monitor API response times

## Getting Help

- Check existing issues and PRs
- Read documentation in README
- Ask in GitHub Discussions
- Open an issue for bugs

## Code of Conduct

- Be respectful and inclusive
- Assume good intent
- Provide constructive feedback
- No spam or harassment
\`\`\`
