# Deployment Checklist for Azure App Service

## Environment Variables
Make sure the following environment variables are set in Azure App Service Configuration:

- `DEBUG`: Set to `True` temporarily to get detailed error messages
- `SECRET_KEY`: Set to a secure random string (different from development)
- `ALLOWED_HOSTS`: Set to your domain names (e.g., `evently-booking.azurewebsites.net,169.254.131.1`)
- `DATABASE_URL`: Set to your PostgreSQL connection string

## SSL/HTTPS Configuration
1. Enable HTTPS Only in Azure App Service settings
2. Ensure custom domains have proper SSL certificates attached
3. Disable HTTP to HTTPS redirection in app settings until you confirm everything is working

## Azure App Service Configuration
1. Check that Python version matches your local development environment
2. Set startup command to: `gunicorn --bind=0.0.0.0 --timeout 600 event_booking.wsgi`
3. Turn on "Always On" feature to prevent the app from unloading
4. Set SCM_DO_BUILD_DURING_DEPLOYMENT to true
5. **Important**: Add health check endpoint in the application to handle Azure's health probe (/robots933456.txt)

## Fixing Azure Health Check Issues
The 500 error is likely caused by Azure's health check system failing. To fix:

1. Add the following to `urls.py` to handle the health check endpoint:
   ```python
   from django.http import HttpResponse
   
   def health_check(request):
       return HttpResponse("OK")
   
   urlpatterns = [
       # Add this at the top of your urlpatterns
       path('robots933456.txt', health_check, name='health_check'),
       
       # ... your existing paths
   ]
   ```

2. Make sure `169.254.131.1` (Azure's health check IP) is included in ALLOWED_HOSTS

## Troubleshooting 500 Server Error
If you're still getting a 500 error after deployment:

1. Check Azure App Service logs (Log stream or Kudu console)
2. Temporarily enable DEBUG mode to see detailed error messages
3. Make sure all required packages are in requirements.txt
4. Check if database migrations are applied correctly
5. Verify Azure has the correct WSGI application path

## Step-by-Step Resolution
1. Temporarily enable DEBUG mode in Azure Configuration
2. Check logs for specific errors
3. Make necessary fixes based on error messages
4. Disable DEBUG mode
5. Restart the App Service
6. Clear your browser cache completely
7. Test with a new private browser window

## Database
1. Ensure database migrations are applied on the production database
2. Run `python manage.py migrate` command in Azure Kudu console if needed
3. Verify database connection is working

## Static Files
1. Make sure WhiteNoise is configured correctly
2. Check that static files are being served properly
3. Run `python manage.py collectstatic` in the Kudu console if needed 