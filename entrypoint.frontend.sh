#!/bin/sh

set -e

# Checagem de variáveis essenciais
if [ -z "$ENVIRONMENT" ]; then
    echo "Error: ENVIRONMENT variable is not set. Exiting..."
    exit 1
fi

echo "Starting frontend setup..."

if [ "$ENVIRONMENT" = "development" ]; then
    echo "Running Vue.js development server..."
    exec npm run serve -- --port $NODE_PORT
elif [ "$ENVIRONMENT" = "production" ]; then
    echo "Building Vue.js project for production..."
    exec npm run build
else
    echo "Error: Invalid ENVIRONMENT value. Must be 'development' or 'production'. Exiting..."
    exit 1
fi
