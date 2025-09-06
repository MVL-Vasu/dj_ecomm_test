# api/wsgi.py
import os, sys
from django.core.wsgi import get_wsgi_application

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

application = get_wsgi_application()
app = application   # Vercel looks for 'app'
