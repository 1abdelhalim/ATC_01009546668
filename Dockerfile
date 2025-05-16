# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=event_booking.settings_postgres
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a startup script with proper PostgreSQL waiting and error handling
RUN echo '#!/bin/bash\n\
\n\
echo "Checking environment variables..."\n\
if [ -z "$DATABASE_URL" ]; then\n\
    echo "ERROR: DATABASE_URL is not set"\n\
    exit 1\n\
fi\n\
\n\
echo "Extracting database connection info..."\n\
DB_HOST=$(echo $DATABASE_URL | sed -n "s/.*@\\(.*\\)\\/.*/\\1/p")\n\
DB_NAME=$(echo $DATABASE_URL | sed -n "s/.*\\/\\([^\?]*\\).*/\\1/p")\n\
\n\
echo "Current directory and files:"\n\
pwd\n\
ls -la\n\
\n\
echo "Python path:"\n\
python -c "import sys; print(sys.path)"\n\
\n\
echo "Waiting for PostgreSQL to be ready..."\n\
until pg_isready -h $DB_HOST -q; do\n\
    echo "PostgreSQL is unavailable - sleeping"\n\
    sleep 2\n\
done\n\
\n\
echo "PostgreSQL is up - executing migrations"\n\
PYTHONPATH=/app python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }\n\
\n\
echo "Collecting static files"\n\
PYTHONPATH=/app python manage.py collectstatic --noinput || { echo "Static files collection failed"; exit 1; }\n\
\n\
echo "Starting Gunicorn"\n\
exec gunicorn --bind 0.0.0.0:${PORT:-8000} \\\n\
    --workers=2 \\\n\
    --threads=4 \\\n\
    --timeout=120 \\\n\
    --access-logfile - \\\n\
    --error-logfile - \\\n\
    --log-level debug \\\n\
    event_booking.wsgi:application\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"] 