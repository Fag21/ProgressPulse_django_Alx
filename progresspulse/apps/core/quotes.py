import requests
from django.core.cache import cache
from django.conf import settings

def get_daily_quote():
    """Fetch a random inspirational quote from the Quotable API"""
    # Try to get from cache first
    cached_quote = cache.get('daily_quote')
    if cached_quote:
        return cached_quote
    
    try:
        # Make API request
        response = requests.get('https://api.quotable.io/random?maxLength=100')
        response.raise_for_status()
        
        quote_data = response.json()
        quote = {
            'content': quote_data['content'],
            'author': quote_data['author'],
        }
        
        # Cache for 24 hours
        cache.set('daily_quote', quote, timeout=60*60*24)
        return quote
        
    except (requests.RequestException, KeyError):
        # Fallback quote if API fails
        return {
            'content': 'The journey of a thousand miles begins with a single step.',
            'author': 'Lao Tzu'
        }