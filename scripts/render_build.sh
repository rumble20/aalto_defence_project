#!/bin/bash
# Render Build Script - Initialize database on first deploy

echo "🚀 Starting Render build process..."

# Check if DATABASE_URL is set (indicates PostgreSQL environment)
if [ -n "$DATABASE_URL" ]; then
    echo "📦 PostgreSQL detected - initializing database..."
    python database/init_postgres.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Database initialized successfully!"
    else
        echo "❌ Database initialization failed!"
        exit 1
    fi
else
    echo "ℹ️  No DATABASE_URL found - skipping database initialization"
    echo "ℹ️  (Local development uses SQLite)"
fi

echo "✅ Build completed successfully!"
exit 0
