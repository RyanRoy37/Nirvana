#!/bin/bash

# Variables - adjust as needed
CONTAINER_NAME="postgres"
DB_USER="postgres"
DB_NAME="nirvana1"

# Paths to your SQL files
SCHEMA_FILE="db/schema.sql"

echo "Creating database '$DB_NAME'..."
echo "Applying schema..."
cat $SCHEMA_FILE | docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME
echo "Database initialization complete."
