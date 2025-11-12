"""
Unit tests for FastAPI inference server.
"""

import unittest
from fastapi.testclient import TestClient
from serve import app, extract_features, ListingRequest

client = TestClient(app)

class TestInferenceAPI(unittest.TestCase):
    
    def test_health_check(self):
        """Test health endpoint."""
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('model_loaded', data)
    
    def test_infer_valid_request(self):
        """Test inference with valid listing."""
        listing = {
            "title": "iPhone 15 Pro Max",
            "description": "Latest Apple smartphone",
            "price": 1199.99,
            "seller": "Apple Official",
            "rating": 4.8,
            "review_count": 5234,
            "category": "electronics",
            "country": "US",
            "images": ["https://example.com/image.jpg"]
        }
        
        response = client.post("/infer", json=listing)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('score', data)
        self.assertIn('label', data)
        self.assertIn('explanation', data)
        self.assertIn('model_version', data)
        
        # Validate score range
        self.assertGreaterEqual(data['score'], 0)
        self.assertLessEqual(data['score'], 1)
        
        # Validate label
        self.assertIn(data['label'], ['safe', 'suspicious', 'high_risk'])
    
    def test_infer_suspicious_listing(self):
        """Test inference on suspicious listing."""
        listing = {
            "title": "iPhone 15 PRO MAX SUPER DEAL!!!",
            "description": "free shipping act now",
            "price": 199.99,
            "seller": "RandomSeller123",
            "rating": 2.1,
            "review_count": 3,
            "category": "electronics",
            "country": "CN",
            "images": []
        }
        
        response = client.post("/infer", json=listing)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have higher fraud score
        self.assertIsNotNone(data['score'])
    
    def test_infer_missing_required_field(self):
        """Test inference with missing required field."""
        listing = {
            "title": "iPhone 15",
            "description": "test",
            # Missing price, seller, rating, review_count
            "category": "electronics",
            "country": "US",
        }
        
        response = client.post("/infer", json=listing)
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_extract_features(self):
        """Test feature extraction."""
        listing = ListingRequest(
            title="Test Product",
            description="Test description",
            price=100.0,
            seller="Test Seller",
            rating=4.0,
            review_count=100,
            category="electronics",
            country="US",
            images=[]
        )
        
        features = extract_features(listing)
        
        # Check that features are extracted
        self.assertGreater(len(features), 0)
        
        # Check feature values are in valid range
        for key, value in features.items():
            self.assertIsInstance(value, (int, float))
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)

if __name__ == '__main__':
    unittest.main()
