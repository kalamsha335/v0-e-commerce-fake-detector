"""
Unit tests for feature extraction module.
"""

import unittest
import pandas as pd
from features import FeatureExtractor

class TestFeatureExtraction(unittest.TestCase):
    
    def setUp(self):
        self.extractor = FeatureExtractor()
        self.sample_df = pd.DataFrame([
            {
                'title': 'iPhone 15 Pro Max',
                'description': 'Latest Apple smartphone',
                'price': 1199.99,
                'seller': 'Apple Official',
                'rating': 4.8,
                'review_count': 5234,
                'category': 'electronics',
                'country': 'US',
                'images': ['img1.jpg', 'img2.jpg'],
            }
        ])
        self.extractor.fit(self.sample_df)
    
    def test_suspicious_words(self):
        """Test detection of suspicious words."""
        listing = {
            'title': 'FREE AMAZING DEAL!!!',
            'description': 'Limited stock act now',
            'price': 99.99,
            'seller': 'test',
            'rating': 3.0,
            'review_count': 10,
            'category': 'electronics',
            'country': 'US',
            'images': [],
        }
        features = self.extractor.extract(listing)
        self.assertGreater(features['suspicious_words_in_title'], 0)
    
    def test_price_anomaly(self):
        """Test price anomaly detection."""
        listing = {
            'title': 'iPhone',
            'description': 'test',
            'price': 50.0,  # Suspiciously low
            'seller': 'test',
            'rating': 3.0,
            'review_count': 10,
            'category': 'electronics',
            'country': 'US',
            'images': [],
        }
        features = self.extractor.extract(listing)
        self.assertEqual(features['price_suspiciously_low'], 1.0)
    
    def test_rating_anomaly(self):
        """Test rating anomaly detection."""
        listing = {
            'title': 'test',
            'description': 'test',
            'price': 100.0,
            'seller': 'test',
            'rating': 4.95,
            'review_count': 2,  # Perfect rating with few reviews
            'category': 'electronics',
            'country': 'US',
            'images': [],
        }
        features = self.extractor.extract(listing)
        self.assertEqual(features['perfect_rating_low_reviews'], 1.0)
    
    def test_no_images(self):
        """Test detection of listings with no images."""
        listing = {
            'title': 'test',
            'description': 'test',
            'price': 100.0,
            'seller': 'test',
            'rating': 3.0,
            'review_count': 10,
            'category': 'electronics',
            'country': 'US',
            'images': [],
        }
        features = self.extractor.extract(listing)
        self.assertEqual(features['no_images'], 1.0)

if __name__ == '__main__':
    unittest.main()
