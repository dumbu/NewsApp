#!/bin/bash
# Setup and test script for NewsApp

echo "🚀 NewsApp Setup & Test Script"
echo "=============================="
echo ""

# Step 1: Verify Docker installation
echo "Step 1: Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi
echo "✅ Docker is installed"
echo ""

# Step 2: Build Docker image
echo "Step 2: Building Docker image..."
cd "/Users/saptagirisa/SAPTA/WORK/NA AI COE/APP"
docker build -t newsapp:0.1.0 .
if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi
echo "✅ Docker image built successfully"
echo ""

# Step 3: Verify modules
echo "Step 3: Verifying all modules can import..."
docker run --rm newsapp:0.1.0 /app/venv/bin/python -c "
from src.models import Article, Category
from src.config import ConfigManager
from src.api import NewsHandler
from src.cache import CacheManager
from src.ui.settings import SettingsView
print('✅ All modules imported successfully')
"
if [ $? -ne 0 ]; then
    echo "❌ Module import failed"
    exit 1
fi
echo ""

# Step 4: List files in git
echo "Step 4: Checking git status..."
git status --short
echo ""

# Step 5: Show last commits
echo "Step 5: Recent commits:"
git log --oneline -5
echo ""

echo "🎉 Setup complete! Run './newsapp' to start the app"
echo ""
echo "Features:"
echo "  • Press 1-5 to select category (US, World, Tech, Business, Science)"
echo "  • Press S to open Settings"
echo "  • Press Q to quit"
echo ""
echo "Settings:"
echo "  • View RSS feed URLs for each category"
echo "  • Edit/add custom feed URLs"
echo "  • Save changes back to config"
