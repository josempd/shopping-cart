#!/bin/bash

# entrypoint.sh
set -e
echo "Connecting to database host: $POSTGRES_HOST"
# Wait for the database to be ready
./wait-for-db.sh $POSTGRES_HOST -- echo "Database is ready!"

# Initialize the database tables based on SQLAlchemy models
echo "Initializing the database schema..."
python init_db.py

# Start the FastAPI application
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --reload
