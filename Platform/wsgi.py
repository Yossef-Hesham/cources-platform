import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Platform.settings')

application = get_wsgi_application()

# Add this for WhiteNoise
from whitenoise import WhiteNoise
application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), 'staticfiles_build/static'))