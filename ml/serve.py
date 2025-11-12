"""
FastAPI server for ML model inference.
Exposes REST API endpoints for fake product detection.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pickle
import os
import logging
import numpy as np
import pandas as pd
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= Pydantic Models =============

class ListingRequest(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    seller: str = Field(..., description="Seller name")
    rating: float = Field(..., ge=0, le=5, description="Product rating 0-5")
    review_count: int = Field(..., ge=0, description="Number of reviews")
    category: str = Field(..., description="Product category")
    country: str = Field(..., description="Country code")
    images: Optional[List[str]] = Field(default=[], description="Image URLs")


class ExplanationItem(BaseModel):
    feature: str
    contribution: float


class AnalysisResponse(BaseModel):
    score: float = Field(..., ge=0, le=1, description="Fraud score 0-1")
    label: str = Field(..., description="safe | suspicious | high_risk")
    explanation: List[ExplanationItem]
    model_version: str
    timestamp: str
    processing_time_ms: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str


# ============= Model Loading =============

def load_model():
    """Load trained model and preprocessing artifacts."""
    try:
        model_path = os.getenv('MODEL_PATH', '/app/models/fake_detector_v0.1.pkl')
        
        if not os.path.exists(model_path):
            logger.warning(f"Model not found at {model_path}, using mock mode")
            return None
        
        with open(model_path, 'rb') as f:
            artifacts = pickle.load(f)
        
        logger.info("Model loaded successfully")
        return artifacts
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return None


# ============= Feature Extraction =============

def extract_features(listing: ListingRequest) -> Dict[str, float]:
    """Extract features from listing for model inference."""
    features = {}
    
    # Text features
    title = listing.title.lower()
    description = (listing.description or '').lower()
    
    suspicious_words = ['free', 'wow', 'amazing', 'limited', 'urgent', 'exclusive', 'fake', 'replica']
    suspicious_in_title = sum(1 for word in suspicious_words if word in title)
    features['suspicious_words_in_title'] = min(suspicious_in_title / 3.0, 1.0)
    
    if len(title) > 0:
        features['title_caps_ratio'] = sum(1 for c in title if c.isupper()) / len(title)
    else:
        features['title_caps_ratio'] = 0.0
    
    special_chars = len([c for c in title if not c.isalnum() and c not in ' '])
    features['title_special_char_density'] = min(special_chars / max(len(title), 1) / 0.1, 1.0)
    features['exclamation_marks'] = min(title.count('!') / 2.0, 1.0)
    features['description_has_url'] = 1.0 if 'http' in description else 0.0
    features['title_length_normalized'] = min(len(title) / 100.0, 1.0)
    features['description_length_normalized'] = min(len(description) / 500.0, 1.0)
    
    # Price features
    category_price_ranges = {
        'electronics': (200, 2000),
        'clothing': (10, 200),
        'jewelry': (50, 5000),
        'watches': (100, 10000),
        'books': (5, 50),
    }
    price_range = category_price_ranges.get(listing.category, (1, 10000))
    median_price = (price_range[0] + price_range[1]) / 2
    
    if median_price > 0:
        price_deviation = abs(listing.price - median_price) / median_price
        features['price_deviation_from_median'] = min(price_deviation, 1.0)
    else:
        features['price_deviation_from_median'] = 0.0
    
    features['price_suspiciously_low'] = 1.0 if listing.price < price_range[0] * 0.3 else 0.0
    features['price_suspiciously_high'] = 1.0 if listing.price > price_range[1] * 2 else 0.0
    
    # Rating features
    features['perfect_rating_low_reviews'] = 1.0 if (listing.rating >= 4.9 and listing.review_count < 10) else 0.0
    features['very_low_rating'] = 1.0 if listing.rating < 2.0 else 0.0
    
    if listing.review_count > 0:
        review_rating_ratio = listing.review_count / (listing.rating * 1000) if listing.rating > 0 else listing.review_count / 1000
        features['review_rating_ratio_anomaly'] = min(abs(1 - review_rating_ratio) / 2, 1.0)
    else:
        features['review_rating_ratio_anomaly'] = 0.0
    
    features['zero_reviews'] = 1.0 if listing.review_count == 0 else 0.0
    features['rating_normalized'] = listing.rating / 5.0
    
    # Seller features
    seller = listing.seller.lower()
    generic_names = ['seller', 'shop', 'store', 'mall', 'market', 'trader']
    is_generic = sum(1 for name in generic_names if name in seller) > 0
    features['generic_seller_name'] = 1.0 if is_generic else 0.0
    
    has_numbers = sum(1 for c in seller if c.isdigit()) / max(len(seller), 1)
    features['seller_name_digit_ratio'] = min(has_numbers, 1.0)
    
    official_keywords = ['official', 'authentic', 'direct', 'store', 'brand']
    is_official = sum(1 for kw in official_keywords if kw in seller) > 0
    features['official_seller_indicator'] = 1.0 if is_official else 0.0
    
    # Image features
    features['no_images'] = 1.0 if len(listing.images) == 0 else 0.0
    features['very_few_images'] = 1.0 if len(listing.images) < 2 else 0.0
    features['many_images'] = 1.0 if len(listing.images) > 10 else 0.0
    
    return features


def get_explanation(features: Dict[str, float], feature_importance: Dict[str, float]) -> List[ExplanationItem]:
    """Generate explanation for prediction."""
    explanations = []
    
    # Get top contributing features
    contributions = []
    for feature, importance in feature_importance.items():
        if feature in features:
            contribution = features[feature] * importance
            contributions.append((feature, contribution))
    
    # Sort by contribution and return top 5
    contributions.sort(key=lambda x: x[1], reverse=True)
    
    for feature, contribution in contributions[:5]:
        explanations.append(ExplanationItem(
            feature=feature,
            contribution=max(0, min(1, contribution))  # Normalize to 0-1
        ))
    
    return explanations


# ============= FastAPI App =============

app = FastAPI(
    title="Fake Product Detector API",
    description="ML model inference API for e-commerce fraud detection",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
model_artifacts = load_model()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        model_loaded=model_artifacts is not None,
        model_version="v0.1"
    )


@app.post("/infer", response_model=AnalysisResponse)
async def infer(listing: ListingRequest):
    """Run inference on a listing."""
    start_time = datetime.now()
    
    try:
        # Extract features
        features = extract_features(listing)
        
        # Prepare feature vector
        feature_names = sorted(features.keys())
        feature_vector = np.array([features[f] for f in feature_names]).reshape(1, -1)
        
        if model_artifacts is None:
            # Mock prediction
            score = np.random.random()
        else:
            # Real prediction
            model = model_artifacts['model']
            scaler = model_artifacts['scaler']
            feature_vector_scaled = scaler.transform(feature_vector)
            score = model.predict_proba(feature_vector_scaled)[0, 1]  # Probability of fake
        
        # Determine label
        if score < 0.4:
            label = "safe"
        elif score < 0.7:
            label = "suspicious"
        else:
            label = "high_risk"
        
        # Generate explanation
        feature_importance = {f: 1/len(features) for f in features}  # Uniform importance for mock
        explanation = get_explanation(features, feature_importance)
        
        # Calculate processing time
        processing_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        return AnalysisResponse(
            score=float(score),
            label=label,
            explanation=explanation,
            model_version="v0.1",
            timestamp=datetime.now().isoformat(),
            processing_time_ms=processing_time_ms
        )
    
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch-infer")
async def batch_infer(listings: List[ListingRequest]):
    """Run inference on multiple listings."""
    results = []
    for listing in listings:
        result = await infer(listing)
        results.append(result)
    return {"results": results, "count": len(results)}


@app.get("/")
async def root():
    """API documentation."""
    return {
        "name": "Fake Product Detector API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "infer": "/infer (POST)",
            "batch_infer": "/batch-infer (POST)",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
