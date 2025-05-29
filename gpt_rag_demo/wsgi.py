import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gpt_rag_demo.settings')

application = get_wsgi_application()
