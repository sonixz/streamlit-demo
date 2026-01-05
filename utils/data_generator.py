import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sales_data(days=30):
    """Generate sample sales data for the specified number of days."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')
    data = []

    for date in dates:
        # Simulate weekly patterns (higher sales on weekends)
        day_multiplier = 1.2 if date.weekday() >= 5 else 1.0

        base_sales = 100 * day_multiplier
        sales = max(10, int(base_sales + random.gauss(0, 30)))

        data.append({
            'date': date,
            'sales': sales,
            'revenue': sales * random.uniform(20, 80),
            'customers': max(5, int(sales * random.uniform(0.3, 0.8))),
            'avg_order_value': random.uniform(25, 150)
        })

    return pd.DataFrame(data)

def generate_user_data(days=30):
    """Generate sample user engagement data."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')
    data = []

    for date in dates:
        active_users = random.randint(500, 2000)
        data.append({
            'date': date,
            'active_users': active_users,
            'new_users': max(10, int(active_users * random.uniform(0.05, 0.15))),
            'returning_users': active_users - max(10, int(active_users * random.uniform(0.05, 0.15))),
            'session_duration': random.uniform(120, 600),
            'page_views': active_users * random.randint(2, 8),
            'bounce_rate': random.uniform(0.2, 0.7)
        })

    return pd.DataFrame(data)

def generate_product_data():
    """Generate sample product performance data."""
    products = [
        "Laptop Pro 15", "Smartphone X", "Tablet Ultra", "Headphones Premium",
        "Camera DSLR", "Monitor 4K", "Keyboard Mechanical", "Mouse Wireless",
        "Speaker Bluetooth", "Watch Smart"
    ]

    data = []
    for product in products:
        data.append({
            'product': product,
            'units_sold': random.randint(50, 500),
            'revenue': random.uniform(5000, 50000),
            'rating': random.uniform(3.5, 5.0),
            'reviews': random.randint(10, 200),
            'category': random.choice(['Electronics', 'Accessories', 'Computers', 'Audio'])
        })

    return pd.DataFrame(data)

def generate_marketing_data(days=30):
    """Generate sample marketing campaign data."""
    channels = ['Google Ads', 'Facebook', 'Instagram', 'LinkedIn', 'Twitter', 'Email', 'SEO', 'Direct']
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='D')

    data = []
    for date in dates:
        for channel in channels:
            spend = random.uniform(100, 1000)
            impressions = int(spend * random.uniform(50, 200))
            clicks = int(impressions * random.uniform(0.01, 0.05))
            conversions = int(clicks * random.uniform(0.02, 0.08))

            data.append({
                'date': date,
                'channel': channel,
                'spend': spend,
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'cpc': spend / clicks if clicks > 0 else 0,
                'ctr': clicks / impressions if impressions > 0 else 0,
                'conversion_rate': conversions / clicks if clicks > 0 else 0
            })

    return pd.DataFrame(data)