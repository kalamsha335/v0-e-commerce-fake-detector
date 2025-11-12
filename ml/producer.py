"""
Simulated data producer for realtime fraud detection demo.
Generates synthetic product listings and sends them to the backend API.
"""

import json
import time
import random
import requests
from datetime import datetime
from typing import Dict, Any, List

class ListingProducer:
    """Generate synthetic product listings for testing."""
    
    PRODUCTS = [
        "iPhone", "Samsung Galaxy", "MacBook Pro", "iPad", "Apple Watch",
        "Nike Shoes", "Adidas Sneakers", "Coach Bag", "Gucci Belt",
        "Diamond Ring", "Gold Necklace", "Rolex Watch", "Cartier Ring",
        "Harry Potter Book", "The Great Gatsby", "To Kill a Mockingbird"
    ]
    
    SELLERS_LEGIT = [
        "Apple Official", "Samsung Direct", "Nike Store",
        "Amazon Basics", "Best Electronics", "TechMart Pro",
        "Authenticated Deals", "Brand Direct Store"
    ]
    
    SELLERS_FAKE = [
        "SuperSeller123", "MegaDeals99", "RandomStore456",
        "CheapStuff789", "WeirdShop01", "MarketTrader2000",
        "UnknownSeller", "TempShop"
    ]
    
    CATEGORIES = ["electronics", "clothing", "jewelry", "watches", "books"]
    COUNTRIES = ["US", "IN", "CN", "UK", "CA"]
    
    def __init__(self, fake_rate: float = 0.3):
        """
        Initialize producer.
        
        Args:
            fake_rate: Probability of generating a fake listing (0-1)
        """
        self.fake_rate = fake_rate
    
    def generate_listing(self) -> Dict[str, Any]:
        """Generate a random product listing."""
        is_fake = random.random() < self.fake_rate
        category = random.choice(self.categories)
        
        if is_fake:
            # Generate suspicious listing
            listing = self._generate_fake_listing(category)
        else:
            # Generate legitimate listing
            listing = self._generate_legit_listing(category)
        
        return listing
    
    def _generate_fake_listing(self, category: str) -> Dict[str, Any]:
        """Generate a suspicious/fake listing."""
        product_base = random.choice(self.PRODUCTS)
        
        title = f"{product_base.upper()} SUPER DEAL!!! {random.choice(['LIMITED', 'EXCLUSIVE', 'MUST SEE'])}"
        if random.random() > 0.5:
            title = title.replace("!", "!!! ") * random.randint(1, 3)
        
        description = random.choice([
            "best price ever buy now",
            "free shipping limited stock",
            "act now offer ends soon",
            "unbelievable price guaranteed authentic",
            "amazing deal dont miss",
            "wow incredible savings",
            "special offer just for you"
        ])
        
        # Suspiciously low price
        category_prices = {
            'electronics': (50, 300),
            'clothing': (5, 50),
            'jewelry': (10, 200),
            'watches': (20, 300),
            'books': (1, 15),
        }
        price_range = category_prices.get(category, (10, 200))
        price = random.uniform(price_range[0] * 0.1, price_range[0] * 0.3)
        
        seller = random.choice(self.SELLERS_FAKE)
        rating = random.choice([1.0, 1.5, 2.0, 4.8, 4.9, 5.0])  # Bimodal
        review_count = random.choice([0, 1, 2, 3, random.randint(5000, 10000)])
        
        return {
            'title': title,
            'description': description,
            'price': round(price, 2),
            'seller': seller,
            'rating': round(rating, 1),
            'review_count': review_count,
            'category': category,
            'country': random.choice(['CN', 'IN']),  # Higher fake rate from these countries
            'images': [] if random.random() > 0.5 else [f'img{i}.jpg' for i in range(random.randint(1, 3))],
        }
    
    def _generate_legit_listing(self, category: str) -> Dict[str, Any]:
        """Generate a legitimate listing."""
        product_base = random.choice(self.PRODUCTS)
        
        title = f"{product_base} - {random.choice(['Premium', 'Authentic', 'Official', 'New'])}"
        
        description = random.choice([
            "Authentic product, brand new in box",
            "Official seller with 10+ years experience",
            "Premium quality guaranteed",
            "Satisfaction guaranteed or money back",
            "Tested and verified authentic"
        ])
        
        # Normal pricing
        category_prices = {
            'electronics': (200, 2000),
            'clothing': (20, 200),
            'jewelry': (100, 5000),
            'watches': (300, 10000),
            'books': (8, 50),
        }
        price_range = category_prices.get(category, (20, 500))
        price = random.uniform(price_range[0], price_range[1])
        
        seller = random.choice(self.SELLERS_LEGIT)
        rating = random.uniform(3.8, 5.0)
        review_count = random.randint(100, 10000)
        
        return {
            'title': title,
            'description': description,
            'price': round(price, 2),
            'seller': seller,
            'rating': round(rating, 1),
            'review_count': review_count,
            'category': category,
            'country': random.choice(['US', 'UK', 'CA']),  # Lower fake rate
            'images': [f'img{i}.jpg' for i in range(random.randint(3, 8))],
        }


def send_to_api(listing: Dict[str, Any], api_url: str = 'http://localhost:3000/api/analyze'):
    """Send listing to backend API for analysis."""
    try:
        response = requests.post(api_url, json=listing, timeout=10)
        result = response.json()
        return {
            'listing': listing,
            'result': result,
            'status': 'success'
        }
    except Exception as e:
        return {
            'listing': listing,
            'error': str(e),
            'status': 'error'
        }


def run_producer(
    duration_seconds: int = 60,
    interval_seconds: float = 3,
    api_url: str = 'http://localhost:3000/api/analyze',
    fake_rate: float = 0.3,
    verbose: bool = True
):
    """
    Run the producer, continuously generating listings and sending to API.
    
    Args:
        duration_seconds: How long to run (0 = infinite)
        interval_seconds: Time between listings
        api_url: Backend API endpoint
        fake_rate: Probability of fake listings
        verbose: Print results
    """
    producer = ListingProducer(fake_rate=fake_rate)
    start_time = datetime.now()
    count = 0
    stats = {'safe': 0, 'suspicious': 0, 'high_risk': 0, 'errors': 0}
    
    print(f"Starting producer (interval: {interval_seconds}s, fake rate: {fake_rate*100:.0f}%)")
    print(f"API: {api_url}")
    print("-" * 80)
    
    try:
        while True:
            # Check duration
            if duration_seconds > 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed > duration_seconds:
                    break
            
            # Generate and send
            listing = producer.generate_listing()
            response = send_to_api(listing, api_url)
            count += 1
            
            if response['status'] == 'success':
                result = response['result']
                label = result.get('label', 'unknown')
                stats[label] = stats.get(label, 0) + 1
                
                if verbose:
                    print(f"[{count}] {listing['title'][:40]:40} | "
                          f"Price: ${listing['price']:7.2f} | "
                          f"Seller: {listing['seller'][:20]:20} | "
                          f"Verdict: {label:10} ({result.get('score', 0)*100:5.1f}%)")
            else:
                stats['errors'] += 1
                if verbose:
                    print(f"[{count}] ERROR: {response.get('error', 'Unknown error')}")
            
            time.sleep(interval_seconds)
    
    except KeyboardInterrupt:
        print("\n" + "-" * 80)
        print("Producer interrupted by user")
    
    # Print stats
    print("\n" + "=" * 80)
    print("FINAL STATISTICS")
    print("=" * 80)
    print(f"Total listings: {count}")
    print(f"Safe: {stats['safe']} ({stats['safe']/max(count,1)*100:.1f}%)")
    print(f"Suspicious: {stats['suspicious']} ({stats['suspicious']/max(count,1)*100:.1f}%)")
    print(f"High Risk: {stats['high_risk']} ({stats['high_risk']/max(count,1)*100:.1f}%)")
    print(f"Errors: {stats['errors']}")
    print(f"Duration: {(datetime.now() - start_time).total_seconds():.1f}s")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run realtime fraud detection producer demo')
    parser.add_argument('--duration', type=int, default=60, help='Duration in seconds (0 = infinite)')
    parser.add_argument('--interval', type=float, default=3, help='Interval between listings (seconds)')
    parser.add_argument('--api-url', default='http://localhost:3000/api/analyze', help='Backend API endpoint')
    parser.add_argument('--fake-rate', type=float, default=0.3, help='Probability of fake listings (0-1)')
    parser.add_argument('--quiet', action='store_true', help='Suppress verbose output')
    
    args = parser.parse_args()
    
    run_producer(
        duration_seconds=args.duration,
        interval_seconds=args.interval,
        api_url=args.api_url,
        fake_rate=args.fake_rate,
        verbose=not args.quiet
    )
