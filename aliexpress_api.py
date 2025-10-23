import requests
import hashlib
import time
import urllib.parse
from config import ALI_APP_KEY, ALI_APP_SECRET, ALI_API_BASE_URL

class AliExpressAPI:
    def __init__(self):
        self.app_key = ALI_APP_KEY
        self.app_secret = ALI_APP_SECRET
        self.base_url = ALI_API_BASE_URL

    def _generate_signature(self, parameters):
        """Generate signature for AliExpress API"""
        sorted_params = sorted(parameters.items())
        query_string = ''.join([f'{k}{v}' for k, v in sorted_params])
        sign_string = self.app_secret + query_string + self.app_secret
        return hashlib.md5(sign_string.encode()).hexdigest().upper()

    def get_product_info(self, product_url):
        """Extract product information from AliExpress URL"""
        try:
            # Extract product ID from URL
            if '/item/' in product_url:
                product_id = product_url.split('/item/')[-1].split('.html')[0]
            else:
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

            # Make API request
            response = requests.get(self.base_url, params=parameters)
            data = response.json()

            if 'error_response' in data:
                print(f"API Error: {data['error_response']}")
                return None

            product_data = data.get('aliexpress_affiliate_product_query_response', {})
            products = product_data.get('resp_result', {}).get('result', {}).get('products', [])
            
            if products:
                return products[0]
            return None

        except Exception as e:
            print(f"Error getting product info: {e}")
            return None

    def generate_affiliate_link(self, original_url, product_id):
        """Generate affiliate link with tracking"""
        from config import AFFILIATE_TRACKING_ID
        
        affiliate_params = {
            'dl_target_url': original_url,
            'aff_short_key': AFFILIATE_TRACKING_ID
        }
        
        query_string = urllib.parse.urlencode(affiliate_params)
        affiliate_link = f"{ALI_AFFILIATE_URL}?{query_string}"
        
        return affiliate_link