"""
Feature extraction module for fake product detection.
Converts raw listing data into ML-ready features.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List, Tuple, Any
import re

class FeatureExtractor:
    """Extract and engineer features from product listings."""
    
    SUSPICIOUS_WORDS = [
        'free', 'wow', 'amazing', 'unbelievable', 'guaranteed', 
        'limited', 'urgent', 'act now', 'exclusive', 'secret',
        'fake', 'replica', 'copy', 'counterfeit', 'imitation'
    ]
    
    def __init__(self):
        self.title_vectorizer = TfidfVectorizer(max_features=20, stop_words='english')
        self.description_vectorizer = TfidfVectorizer(max_features=20, stop_words='english')
        self.fitted = False
    
    def fit(self, df: pd.DataFrame):
        """Fit vectorizers on training data."""
        # Handle missing values
        titles = df['title'].fillna('').astype(str)
        descriptions = df['description'].fillna('').astype(str)
        
        if len(titles) > 0:
            self.title_vectorizer.fit(titles)
        if len(descriptions) > 0:
            self.description_vectorizer.fit(descriptions)
        
        self.fitted = True
    
    def extract(self, listing: Dict[str, Any]) -> Dict[str, float]:
        """Extract features from a single listing."""
        features = {}
        
        # Text features
        features.update(self._extract_text_features(listing))
        
        # Price features
        features.update(self._extract_price_features(listing))
        
        # Rating features
        features.update(self._extract_rating_features(listing))
        
        # Seller features
        features.update(self._extract_seller_features(listing))
        
        # Image features
        features.update(self._extract_image_features(listing))
        
        return features
    
    def _extract_text_features(self, listing: Dict) -> Dict[str, float]:
        """Extract TF-IDF and text-based features."""
        features = {}
        title = listing.get('title', '').lower()
        description = listing.get('description', '').lower()
        
        # Suspicious word count
        suspicious_in_title = sum(1 for word in self.SUSPICIOUS_WORDS if word in title)
        features['suspicious_words_in_title'] = min(suspicious_in_title / 3.0, 1.0)  # Normalize
        
        # All caps ratio
        if len(title) > 0:
            features['title_caps_ratio'] = sum(1 for c in title if c.isupper()) / len(title)
        else:
            features['title_caps_ratio'] = 0.0
        
        # Special character density
        special_chars = len([c for c in title if not c.isalnum() and c not in ' '])
        features['title_special_char_density'] = min(special_chars / max(len(title), 1) / 0.1, 1.0)
        
        # Exclamation marks
        features['exclamation_marks'] = min(title.count('!') / 2.0, 1.0)
        
        # URL in description (suspicious)
        features['description_has_url'] = 1.0 if 'http' in description else 0.0
        
        # Length features
        features['title_length_normalized'] = min(len(title) / 100.0, 1.0)
        features['description_length_normalized'] = min(len(description) / 500.0, 1.0)
        
        return features
    
    def _extract_price_features(self, listing: Dict) -> Dict[str, float]:
        """Extract price anomaly features."""
        features = {}
        price = float(listing.get('price', 0))
        category = listing.get('category', 'unknown')
        
        # Price ranges by category (median prices from market)
        category_price_ranges = {
            'electronics': (200, 2000),
            'clothing': (10, 200),
            'jewelry': (50, 5000),
            'watches': (100, 10000),
            'books': (5, 50),
        }
        
        price_range = category_price_ranges.get(category, (1, 10000))
        median_price = (price_range[0] + price_range[1]) / 2
        
        # Price deviation from median
        if median_price > 0:
            price_deviation = abs(price - median_price) / median_price
            features['price_deviation_from_median'] = min(price_deviation, 1.0)
        else:
            features['price_deviation_from_median'] = 0.0
        
        # Price too low
        features['price_suspiciously_low'] = 1.0 if price < price_range[0] * 0.3 else 0.0
        
        # Price suspiciously high
        features['price_suspiciously_high'] = 1.0 if price > price_range[1] * 2 else 0.0
        
        return features
    
    def _extract_rating_features(self, listing: Dict) -> Dict[str, float]:
        """Extract rating/review anomalies."""
        features = {}
        
        rating = float(listing.get('rating', 0))
        review_count = int(listing.get('review_count', 0))
        
        # Perfect rating with few reviews (suspicious)
        features['perfect_rating_low_reviews'] = 1.0 if (rating >= 4.9 and review_count < 10) else 0.0
        
        # Very low rating with few reviews
        features['very_low_rating'] = 1.0 if rating < 2.0 else 0.0
        
        # Review/rating anomaly
        if review_count > 0:
            review_rating_ratio = review_count / (rating * 1000) if rating > 0 else review_count / 1000
            features['review_rating_ratio_anomaly'] = min(abs(1 - review_rating_ratio) / 2, 1.0)
        else:
            features['review_rating_ratio_anomaly'] = 0.0
        
        # No reviews
        features['zero_reviews'] = 1.0 if review_count == 0 else 0.0
        
        # Rating normalized
        features['rating_normalized'] = rating / 5.0
        
        return features
    
    def _extract_seller_features(self, listing: Dict) -> Dict[str, float]:
        """Extract seller-based features."""
        features = {}
        seller = listing.get('seller', '').lower()
        
        # Generic/random seller names (suspicious)
        generic_names = ['seller', 'shop', 'store', 'mall', 'market', 'trader']
        is_generic = sum(1 for name in generic_names if name in seller) > 0
        features['generic_seller_name'] = 1.0 if is_generic else 0.0
        
        # Seller name with numbers (sometimes suspicious)
        has_numbers = sum(1 for c in seller if c.isdigit()) / max(len(seller), 1)
        features['seller_name_digit_ratio'] = min(has_numbers, 1.0)
        
        # Official/brand name indicators
        official_keywords = ['official', 'authentic', 'direct', 'store', 'brand']
        is_official = sum(1 for kw in official_keywords if kw in seller) > 0
        features['official_seller_indicator'] = 1.0 if is_official else 0.0
        
        return features
    
    def _extract_image_features(self, listing: Dict) -> Dict[str, float]:
        """Extract image-based features."""
        features = {}
        images = listing.get('images', [])
        
        # No images
        features['no_images'] = 1.0 if len(images) == 0 else 0.0
        
        # Very few images
        features['very_few_images'] = 1.0 if len(images) < 2 else 0.0
        
        # Many images (sometimes legitimate)
        features['many_images'] = 1.0 if len(images) > 10 else 0.0
        
        return features


def extract_batch_features(df: pd.DataFrame, extractor: FeatureExtractor) -> pd.DataFrame:
    """Extract features for a batch of listings."""
    features_list = []
    
    for _, row in df.iterrows():
        listing = row.to_dict()
        features = extractor.extract(listing)
        features_list.append(features)
    
    features_df = pd.DataFrame(features_list)
    return features_df
