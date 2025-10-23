import requests
import hashlib
import time
import urllib.parse
import json
from config import ALI_APP_KEY, ALI_APP_SECRET, ALI_API_BASE_URL

class AliExpressAPI:
    def __init__(self):
        self.app_key = 503584
        self.app_secret = X182pgtCLcmACxgUTVb3dhwos8bYrR7Y
        self.base_url = ALI_API_BASE_URL

    def _generate_signature(self, parameters):
        """Generate signature for AliExpress API"""
        sorted_params = sorted(parameters.items())
        query_string = ''.join([f'{k}{v}' for k, v in sorted_params])
        sign_string = self.app_secret + query_string + self.app_secret
        return hashlib.md5(sign_string.encode()).hexdigest().upper()

    def get_product_info(self, product_url):
        """Extract product information from AliExpress URL with detailed debugging"""
        try:
            print(f"🔍 API Debug: Processing URL: {product_url}")
            
            # Extract product ID from URL with multiple methods
            product_id = None
            
            # Method 1: Standard item URLs
            if '/item/' in product_url:
                product_id = product_url.split('/item/')[-1].split('.html')[0]
                print(f"🔍 API Debug: Extracted product ID (method 1): {product_id}")
            
            # Method 2: Alternative pattern
            if not product_id and '.html' in product_url:
                # Look for numbers before .html
                import re
                match = re.search(r'/(\d+)\.html', product_url)
                if match:
                    product_id = match.group(1)
                    print(f"🔍 API Debug: Extracted product ID (method 2): {product_id}")
            
            # Method 3: Any numeric ID in the URL
            if not product_id:
                import re
                numbers = re.findall(r'\d+', product_url)
                if numbers:
                    # Take the longest number (likely the product ID)
                    product_id = max(numbers, key=len)
                    print(f"🔍 API Debug: Extracted product ID (method 3): {product_id}")
            
            if not product_id:
                print("❌ API Debug: Could not extract product ID from URL")
                return None
            
            # Clean product ID - remove any non-numeric characters
            product_id = ''.join(filter(str.isdigit, product_id))
            print(f"🔍 API Debug: Cleaned product ID: {product_id}")
            
            if len(product_id) < 8:  # AliExpress IDs are usually long
                print(f"❌ API Debug: Product ID too short: {product_id}")
                return None

            # API parameters
            method = "aliexpress.affiliate.product.query"
            timestamp = str(int(time.time() * 1000))
            
            parameters = {
                'app_key': self.app_key,
                'method': method,
                'timestamp': timestamp,
                'v': '2.0',
                'sign_method': 'md5',
                'format': 'json',
                'product_ids': product_id,
                'fields': 'product_id,product_title,product_image_url,original_price,sale_price,discount,shop_url,shop_id'
            }

            # Generate signature
            parameters['sign'] = self._generate_signature(parameters)
            
            print(f"🔍 API Debug: Making API request with parameters:")
            print(f"   App Key: {self.app_key[:10]}...")
            print(f"   Product ID: {product_id}")
            print(f"   Timestamp: {timestamp}")

            # Make API request
            response = requests.get(self.base_url, params=parameters, timeout=30)
            print(f"🔍 API Debug: Response status: {response.status_code}")
            
            try:
                data = response.json()
                print(f"🔍 API Debug: Full API response: {json.dumps(data, indent=2)}")
            except:
                print(f"🔍 API Debug: Response text: {response.text}")
                return None

            # Check for API errors
            if 'error_response' in data:
                error_msg = data['error_response']
                print(f"❌ API Error: {error_msg}")
                return None

            # Check for successful response
            product_data = data.get('aliexpress_affiliate_product_query_response', {})
            resp_result = product_data.get('resp_result', {})
            result = resp_result.get('result', {})
            products = result.get('products', [])
            
            print(f"🔍 API Debug: Found {len(products)} products")
            
            if products:
                product_info = products[0]
                print(f"✅ API Debug: Successfully retrieved product: {product_info.get('product_title', 'Unknown')}")
                return product_info
            else:
                print("❌ API Debug: No products found in response")
                return None

        except Exception as e:
            print(f"❌ API Exception: {str(e)}")
            import traceback
            print(f"❌ API Traceback: {traceback.format_exc()}")
            return None

    def generate_affiliate_link(self, original_url, product_id):
        """Generate affiliate link with tracking"""
        from config import AFFILIATE_TRACKING_ID
        
        print(f"🔍 Affiliate Debug: Generating link for product {product_id}")
        
        affiliate_params = {
            'dl_target_url': original_url,
            'aff_short_key': AFFILIATE_TRACKING_ID
        }
        
        query_string = urllib.parse.urlencode(affiliate_params)
        affiliate_link = f"https://s.click.aliexpress.com/deep_link.htm?{query_string}"
        
        print(f"🔍 Affiliate Debug: Generated link: {affiliate_link}")
        return affiliate_link
