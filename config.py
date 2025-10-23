import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '8313212995:AAEluLHLHRbA73wpSxsNd9mKCgg376UAudk')

# AliExpress Affiliate Configuration
ALI_APP_KEY = os.getenv('503584')
ALI_APP_SECRET = os.getenv('ALI_APP_SECRET', 'X182pgtCLcmACxgUTVb3dhwos8bYrR7Y')
AFFILIATE_TRACKING_ID = os.getenv('Coupons_bot', 'Coupons_bot)

# API Endpoints
ALI_API_BASE_URL = "https://api-sg.aliexpress.com/sync"
ALI_AFFILIATE_URL = "https://s.click.aliexpress.com/deep_link.htm"