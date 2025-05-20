#!/bin/bash
# run.sh - Setup and run script for the Document Research & Theme Identification Chatbot

# Print colorful messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up Document Research & Theme Identification Chatbot...${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker not found. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${GREEN}Creating necessary directories...${NC}"
mkdir -p backend/app/data/uploads
mkdir -p chroma_store

# Start the services
echo -e "${GREEN}Starting services with Docker Compose...${NC}"
docker-compose up -d

# Wait for Ollama to start
echo -e "${YELLOW}Waiting for Ollama to initialize (this may take a minute)...${NC}"
sleep 20

# Download the Llama3 model for Ollama
echo -e "${GREEN}Downloading LLaMA3 model for Ollama...${NC}"
docker exec -it $(docker ps -qf "name=ollama") ollama pull llama3

echo -e "${GREEN}Setup complete! Services are now running:${NC}"
echo -e "${YELLOW}Frontend UI:${NC} http://localhost:8501"
echo -e "${YELLOW}Backend API:${NC} http://localhost:8000"
echo -e "${YELLOW}API Documentation:${NC} http://localhost:8000/docs"

echo -e "${GREEN}To stop the services, run:${NC} docker-compose down"