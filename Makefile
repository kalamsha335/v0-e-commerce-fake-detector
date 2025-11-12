.PHONY: help install dev build test lint clean docker-build docker-up docker-down producer

help:
	@echo "Fake Product Detector - Available Commands"
	@echo "=========================================="
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Start development server"
	@echo "  make build        - Build for production"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linting"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make docker-up    - Start Docker services"
	@echo "  make docker-down  - Stop Docker services"
	@echo "  make producer     - Run data producer (default 60s)"
	@echo ""

install:
	npm install
	cd ml && pip install -r requirements.txt

dev:
	npm run dev

build:
	npm run build

test:
	npm run lint
	npm run build
	cd ml && python -m pytest test_*.py -v

lint:
	npm run lint
	cd ml && pylint ml/*.py || true

clean:
	rm -rf .next dist build
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

producer:
	@read -p "Duration (seconds) [60]: " duration; \
	read -p "Interval (seconds) [3]: " interval; \
	cd ml && python producer.py \
		--duration $${duration:-60} \
		--interval $${interval:-3} \
		--api-url http://localhost:3000/api/analyze
