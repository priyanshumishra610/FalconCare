#!/bin/bash

# FalconCare - Complete System Startup Script
# Starts both advanced Rasa chatbot and beautiful frontend

echo "🚀 STARTING FALCONCARE COMPLETE SYSTEM"
echo "======================================"
echo "🎯 Advanced AI Health Chatbot for Rural India"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check dependencies
echo "🔍 CHECKING DEPENDENCIES..."
echo "----------------------------"

if command_exists python3; then
    print_status "Python 3 found: $(python3 --version)"
else
    print_error "Python 3 not found. Please install Python 3.8+"
    exit 1
fi

if command_exists node; then
    print_status "Node.js found: $(node --version)"
else
    print_warning "Node.js not found. Frontend won't work without it."
    FRONTEND_AVAILABLE=false
fi

if command_exists npm; then
    print_status "npm found: $(npm --version)"
    FRONTEND_AVAILABLE=true
else
    print_warning "npm not found. Frontend won't work."
    FRONTEND_AVAILABLE=false
fi

# Check if Rasa is installed
if command_exists rasa; then
    print_status "Rasa found: $(rasa --version | head -n1)"
else
    print_info "Installing Rasa..."
    pip install -r requirements.txt
fi

echo ""
echo "📦 INSTALLING/UPDATING DEPENDENCIES..."
echo "--------------------------------------"

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies if available
if [ "$FRONTEND_AVAILABLE" = true ]; then
    print_info "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

echo ""
echo "🧠 TRAINING FALCONCARE MODEL..."
echo "-------------------------------"

# Train the Rasa model
print_info "Training advanced health AI model..."
rasa train --config config.yml --domain domain.yml --data data/

if [ $? -eq 0 ]; then
    print_status "FalconCare model trained successfully!"
else
    print_error "Model training failed"
    exit 1
fi

echo ""
echo "🚀 STARTING FALCONCARE SERVICES..."
echo "----------------------------------"

# Kill any existing services on our ports
print_info "Cleaning up existing services..."
pkill -f "rasa run" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true

sleep 2

# Start Rasa Actions Server (Background)
print_info "Starting Rasa Actions Server (Port 5055)..."
rasa run actions --port 5055 --debug > logs/actions.log 2>&1 &
ACTIONS_PID=$!

sleep 3

# Start Rasa Core Server (Background)  
print_info "Starting Rasa Core Server (Port 5005)..."
rasa run --enable-api --port 5005 --cors "*" --debug > logs/rasa.log 2>&1 &
RASA_PID=$!

sleep 3

# Start Backend API (Background)
print_info "Starting Backend API (Port 5001)..."
python backend/app.py > logs/backend.log 2>&1 &
BACKEND_PID=$!

sleep 2

# Start Frontend (Background)
if [ "$FRONTEND_AVAILABLE" = true ]; then
    print_info "Starting Frontend (Port 5173)..."
    cd frontend && npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    sleep 3
fi

echo ""
echo "🎯 FALCONCARE SYSTEM STATUS"
echo "============================="

# Check service status
if port_in_use 5055; then
    print_status "Actions Server: Running on port 5055"
else
    print_error "Actions Server: Failed to start"
fi

if port_in_use 5005; then
    print_status "Rasa Core: Running on port 5005"
else
    print_error "Rasa Core: Failed to start"
fi

if port_in_use 5001; then
    print_status "Backend API: Running on port 5001" 
else
    print_error "Backend API: Failed to start"
fi

if [ "$FRONTEND_AVAILABLE" = true ] && port_in_use 5173; then
    print_status "Frontend: Running on port 5173"
elif [ "$FRONTEND_AVAILABLE" = true ]; then
    print_error "Frontend: Failed to start"
fi

echo ""
echo "🌐 ACCESS POINTS"
echo "=================="
echo "🤖 Rasa Chat API:    http://localhost:5005"
echo "🌐 Web Frontend:     http://localhost:5173"
echo "📱 Backend API:      http://localhost:5001"
echo "📊 API Health:       http://localhost:5001/api/health"

echo ""
echo "💬 QUICK TESTS"
echo "==============="
echo "Test in terminal: rasa shell"
echo "Or use web interface: http://localhost:5173"
echo ""
print_info "Try these test messages:"
echo "   Hindi: 'नमस्ते' or 'मुझे बुखार है'"
echo "   English: 'hello' or 'I have fever'"
echo "   Emergency: 'सीने में दर्द है'"
echo "   Myth: 'हल्दी से कैंसर ठीक होता है'"

echo ""
echo "🎭 FOR SIH DEMO"
echo "================"
echo "1. Open browser: http://localhost:5173"
echo "2. Click chat button"
echo "3. Test with judges!"
echo ""
echo "🏆 FalconCare is ready to win SIH!"

# Create log directory
mkdir -p logs

# Function to handle cleanup on exit
cleanup() {
    echo ""
    print_info "Shutting down FalconCare services..."
    kill $ACTIONS_PID $RASA_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Keep script running
print_info "Press Ctrl+C to stop all services"
wait