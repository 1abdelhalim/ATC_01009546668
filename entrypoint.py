#!/usr/bin/env python
"""
Entrypoint script for the application.
This validates settings and starts the application.
"""

import os
import sys
import subprocess
import django

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Python path:", sys.path)

# Explicitly add the app directory to Python path
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
    print(f"Added {app_dir} to Python path")

print("Updated Python path:", sys.path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings_postgres')
print("Django settings module:", os.environ.get('DJANGO_SETTINGS_MODULE'))

# Validate Django version
print("Django version:", django.__version__)

# Try to import settings
try:
    from django.conf import settings
    print("Settings imported successfully")
    print("DEBUG setting:", settings.DEBUG)
    print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
    print("DATABASE default ENGINE:", settings.DATABASES['default']['ENGINE'])
    
    # Set up Django
    django.setup()
    print("Django setup completed successfully")
    
    # Migrate database
    print("Running migrations...")
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "migrate", "--noinput"])
    
    # Collect static files
    print("Collecting static files...")
    execute_from_command_line(["manage.py", "collectstatic", "--noinput"])
    
    # Start Gunicorn
    port = os.environ.get('PORT', '80')
    print(f"Starting Gunicorn on port {port}...")
    cmd = [
        "gunicorn",
        "--bind", f"0.0.0.0:{port}",
        "--workers=2",
        "--threads=4",
        "--timeout=120",
        "--access-logfile", "-",
        "--error-logfile", "-",
        "--log-level=debug",
        "event_booking.wsgi:application"
    ]
    subprocess.call(cmd)
    
except Exception as e:
    print(f"Error importing settings: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 