import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Platform.settings')

# Get the Django WSGI application
django_app = get_wsgi_application()

# WhiteNoise configuration
from whitenoise import WhiteNoise
application = WhiteNoise(django_app)

# Required for Vercel
app = application  # This satisfies Vercel's handler requirement