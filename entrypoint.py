#!/usr/bin/env python
"""
Entrypoint script for the application.
This validates settings and starts the application.
"""

import os
import sys
import subprocess
import importlib.util

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Python path:", sys.path)

# List installed packages
try:
    print("\nInstalled packages:")
    subprocess.call(["pip", "freeze"])
except Exception as e:
    print(f"Error listing packages: {e}")

# Explicitly add the app directory to Python path
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)
    print(f"Added {app_dir} to Python path")

print("Updated Python path:", sys.path)

# Ensure required packages are available
required_packages = ['django', 'dj_database_url', 'gunicorn', 'psycopg2']
missing_packages = []

for package in required_packages:
    spec = importlib.util.find_spec(package)
    if spec is None:
        missing_packages.append(package)
        print(f"WARNING: Package {package} is not installed")
    else:
        try:
            module = importlib.import_module(package)
            if hasattr(module, '__version__'):
                print(f"Package {package} is installed, version: {module.__version__}")
            else:
                print(f"Package {package} is installed (no version info)")
        except Exception as e:
            print(f"Error importing {package}: {e}")
            missing_packages.append(package)

if missing_packages:
    print(f"ERROR: Missing required packages: {', '.join(missing_packages)}")
    print("Attempting to install missing packages...")
    for package in missing_packages:
        try:
            subprocess.call([sys.executable, "-m", "pip", "install", package])
            print(f"Installed {package}")
        except Exception as e:
            print(f"Failed to install {package}: {e}")

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_booking.settings_postgres')
print("Django settings module:", os.environ.get('DJANGO_SETTINGS_MODULE'))

# Check if Database URL is set
db_url = os.environ.get('DATABASE_URL')
print(f"Database URL is {'set' if db_url else 'NOT SET'}")
if db_url:
    # Mask password for security in logs
    masked_url = db_url.replace(db_url.split('@')[0], '***:***')
    print(f"Database URL (masked): {masked_url}")

# Try to import settings
try:
    # First try direct import of settings
    print("Trying direct import of settings module...")
    import event_booking.settings_postgres as direct_settings
    print("Direct settings import successful")

    # Now try the Django way
    print("Importing settings via django.conf...")
    import django
    print("Django version:", django.__version__)
    from django.conf import settings
    print("Settings imported successfully")
    print("DEBUG setting:", settings.DEBUG)
    print("ALLOWED_HOSTS:", settings.ALLOWED_HOSTS)
    print("DATABASE default ENGINE:", settings.DATABASES['default']['ENGINE'])
    
    # Set up Django
    django.setup()
    print("Django setup completed successfully")
    
    # Check database connection
    if db_url:
        print("Testing database connection...")
        import psycopg2
        from urllib.parse import urlparse
        
        parsed_url = urlparse(db_url)
        db_host = parsed_url.hostname
        db_port = parsed_url.port or 5432
        db_name = parsed_url.path.lstrip('/')
        db_user = parsed_url.username
        db_password = parsed_url.password
        
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password
            )
            conn.close()
            print("Database connection successful")
        except Exception as e:
            print(f"Database connection failed: {e}")
            print("Will attempt migrations anyway...")
    
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
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 