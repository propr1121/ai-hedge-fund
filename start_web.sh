#!/bin/bash

# AI Hedge Fund Web Interface Startup Script
echo "🚀 Starting AI Hedge Fund Web Interface..."
echo ""

# Add Poetry to PATH
export PATH="/home/ubuntu/.local/bin:$PATH"

# Check if Poetry is available
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry not found. Please install Poetry first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. You may need to add your API keys."
    echo "   Create a .env file with your OpenAI API key to use the hedge fund functionality."
    echo ""
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
poetry install

# Start the web server
echo "🌐 Starting web server on http://172.30.0.2:5000/"
echo ""
echo "✅ Web interface will be available at: http://172.30.0.2:5000/"
echo "🔗 Test endpoint: http://172.30.0.2:5000/test"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask app
poetry run python app.py