import re

def extract_aliexpress_url(text):
    """Extract AliExpress URLs from text"""
    # AliExpress URL patterns
    patterns = [
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/item/\d+\.html',
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/store/product/\d+\.html',
        r'https?://[a-zA-Z]*\.?aliexpress\.\w+/\d+/\d+\.html'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    return None

def format_product_message(product_info, affiliate_link):
    """Format product information for Telegram message"""
    title = product_info.get('product_title', 'Unknown Product')
    original_price = product_info.get('original_price', '0')
    sale_price = product_info.get('sale_price', '0')
    discount = product_info.get('discount', '0')
    image_url = product_info.get('product_image_url', '')
    
    message = f"🛍️ *{title}*\n\n"
    message += f"💰 *Original Price:* ${original_price}\n"
    message += f"🎯 *Sale Price:* ${sale_price}\n"
    message += f"🎁 *Discount:* {discount}%\n\n"
    message += f"🔗 [Get Discounted Price]({affiliate_link})"
    
    return message, image_url