# Realtime Monitoring Demo

This guide explains how to run the realtime fraud detection demo with synthetic product listings.

## Quick Start

### 1. Start All Services

\`\`\`bash
docker-compose up
\`\`\`

This starts:
- Next.js frontend at http://localhost:3000
- Python ML service at http://localhost:8000
- PostgreSQL at localhost:5432

### 2. Run the Producer in Another Terminal

\`\`\`bash
# Using the script
bash scripts/run-producer.sh 60 3 0.3

# Or directly with Python
cd ml
python producer.py --duration 60 --interval 3 --fake-rate 0.3
\`\`\`

**Arguments:**
- `--duration`: How long to run in seconds (default: 60)
- `--interval`: Seconds between listings (default: 3)
- `--fake-rate`: Probability of fake listings 0-1 (default: 0.3)
- `--api-url`: Backend API endpoint (default: http://localhost:3000/api/analyze)
- `--quiet`: Suppress verbose output

### 3. Watch the Monitor

Open http://localhost:3000/monitor in your browser to see listings processed in realtime.

## Example Output

\`\`\`
[1] iPhone SUPER DEAL!!! EXCLUSIVE!!!  | Price: $199.99   | Seller: SuperSeller123 | Verdict: high_risk (87.3%)
[2] Samsung Galaxy - Official        | Price: $899.99   | Seller: Samsung Direct | Verdict: safe      (12.5%)
[3] MacBook PRO LIMITED OFFER!!!      | Price: $150.00   | Seller: CheapStuff789  | Verdict: suspicious (63.2%)
...

==================================================
FINAL STATISTICS
==================================================
Total listings: 30
Safe: 21 (70.0%)
Suspicious: 6 (20.0%)
High Risk: 3 (10.0%)
Errors: 0
Duration: 87.5s
\`\`\`

## Features

- **Synthetic Data Generation**: Creates realistic fake and legitimate listings
- **Configurable Rates**: Adjust fake listing probability
- **Real API Calls**: Each listing goes through the full ML pipeline
- **Statistics Tracking**: Summary of results after completion
- **Error Handling**: Graceful handling of API failures

## Integration

The producer can be:
- Run as a scheduled job in production
- Called from a message queue (Kafka, RabbitMQ)
- Triggered by webhooks from marketplaces
- Chained with other data sources

For production use, integrate with:
- Event streaming platforms (Kafka)
- Cloud functions (AWS Lambda)
- Workflow orchestration (Airflow)
\`\`\`
