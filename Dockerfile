# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=event_booking.settings_production
ENV PYTHONPATH=/app
ENV PORT=80

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly install dj-database-url
RUN pip install --no-cache-dir dj-database-url==2.1.0

# Copy project files
COPY . .

# Debug: Show what files were copied and verify critical files
RUN echo "Current directory structure:" && \
    pwd && \
    ls -la && \
    echo "\nVerifying critical files:" && \
    test -f /app/event_booking/settings_postgres.py || (echo "ERROR: settings_postgres.py not found" && exit 1) && \
    echo "settings_postgres.py found successfully" && \
    test -f /app/entrypoint.py || (echo "ERROR: entrypoint.py not found" && exit 1) && \
    echo "entrypoint.py found successfully" && \
    python -m compileall /app/event_booking

# Set a build-time SECRET_KEY for collectstatic (not used at runtime)
ENV SECRET_KEY="build-time-secret-key-for-collectstatic-only"

# Collect static files
RUN echo "Collecting static files..." && \
    mkdir -p /app/staticfiles/img/sections && \
    cp -f /app/static/img/sections/app-download.jpg /app/staticfiles/img/sections/ && \
    python manage.py collectstatic --noinput --verbosity 1 && \
    # Verify key static files exist
    ls -la /app/staticfiles/img/sections/

# Verify packages (without failing the build)
RUN echo "Checking for dj-database-url package:" && \
    pip freeze | grep -i dj-database-url || echo "Package not found in pip freeze" && \
    echo "Attempting to import dj_database_url:" && \
    python -c "import dj_database_url; print('dj-database-url imported successfully')" || echo "Import failed"

# Remove the build-time SECRET_KEY
ENV SECRET_KEY=""

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.py

# Run the entrypoint script
CMD ["python", "/app/entrypoint.py"] 