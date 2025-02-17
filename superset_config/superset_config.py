import os

# Superset specific config
ROW_LIMIT = 5000

# Flask App Builder configuration
SECRET_KEY = "1234"

# The SQLAlchemy connection string to your metadata database
SQLALCHEMY_DATABASE_URI = 'sqlite:////var/lib/superset/superset.db'

# Flask-WTF flag for CSRF
CSRF_ENABLED = True

# Use Redis to store the results of queries
RESULTS_BACKEND = None

# Mapbox API key
MAPBOX_API_KEY = ''