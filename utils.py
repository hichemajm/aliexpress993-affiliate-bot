import re

def extract_aliexpress_url(text):
    """Extract AliExpress URLs from text with improved pattern matching"""
    
    # Improved AliExpress URL patterns
    patterns = [
        # Standard product URLs
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/item/\d+\.html\S*',
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/store/product/\d+\.html\S*',
        
        # Mobile app share links
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/\w+/\d+\.html\S*',
        
        # URLs with parameters
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/item/\d+\.html\?[^\s]*',
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/\w+/\d+\.html\?[^\s]*',
        
        # Shortened AliExpress links
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/[a-zA-Z0-9]+\?[^\s]*',
        
        # New style URLs
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/\w+/[a-zA-Z0-9]+\.html\S*'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            # Clean the URL by removing any trailing characters that aren't part of the URL
            url = matches[0]
            # Remove common trailing punctuation
            url = re.sub(r'[.,!?;:]$', '', url)
            return url
    
    return None

# Alternative simpler approach - use this if above doesn't work
def extract_aliexpress_url_simple(text):
    """Simple but effective AliExpress URL extraction"""
    # Look for any URL containing aliexpress and /item/ or /product/
    pattern = r'https?://[^\s]*aliexpress[^\s]*(?:/item/|/product/|/i/)[^\s]*'
    
    matches = re.findall(pattern, text, re.IGNORECASE)
    if matches:
        url = matches[0]
        # Clean up URL
        url = re.sub(r'[<>]', '', url)  # Remove < and > if any
        return url
    
    return None

# Use the simple version for better detection
def extract_aliexpress_url(text):
    return extract_aliexpress_url_simple(text)
