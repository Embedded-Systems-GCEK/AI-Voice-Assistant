#!/bin/bash

# AI Voice Assistant API Test Script
# This script tests all major API endpoints

set -e  # Exit on error

BASE_URL="http://localhost:5000"
TEST_USERNAME="test_user_$$"
TEST_EMAIL="test_$$@example.com"

echo "=========================================="
echo "AI Voice Assistant API Test Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print success
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print error
error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to print info
info() {
    echo -e "${YELLOW}→${NC} $1"
}

# Test 1: Health Check
echo "Test 1: Health Check"
info "GET /health"
if curl -s -f "$BASE_URL/health" > /dev/null; then
    success "Health check passed"
else
    error "Health check failed"
    exit 1
fi
echo ""

# Test 2: Ping
echo "Test 2: Ping"
info "GET /ping"
if curl -s -f "$BASE_URL/ping" > /dev/null; then
    success "Ping test passed"
else
    error "Ping test failed"
    exit 1
fi
echo ""

# Test 3: Create User
echo "Test 3: Create User"
info "POST /users"
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$TEST_USERNAME\",\"email\":\"$TEST_EMAIL\"}")

if echo "$USER_RESPONSE" | grep -q "success"; then
    USER_ID=$(echo "$USER_RESPONSE" | jq -r '.data.user.id')
    success "User created with ID: $USER_ID"
else
    error "Failed to create user"
    echo "$USER_RESPONSE"
    exit 1
fi
echo ""

# Test 4: Get All Users
echo "Test 4: Get All Users"
info "GET /users"
if curl -s -f "$BASE_URL/users" | grep -q "$TEST_USERNAME"; then
    success "Successfully retrieved users list"
else
    error "Failed to get users"
    exit 1
fi
echo ""

# Test 5: Get User by ID
echo "Test 5: Get User by ID"
info "GET /users/$USER_ID"
if curl -s -f "$BASE_URL/users/$USER_ID" | grep -q "$TEST_USERNAME"; then
    success "Successfully retrieved user details"
else
    error "Failed to get user details"
    exit 1
fi
echo ""

# Test 6: Get Example Questions
echo "Test 6: Get Example Questions"
info "GET /api/example-questions"
if curl -s -f "$BASE_URL/api/example-questions" | grep -q "example"; then
    success "Successfully retrieved example questions"
else
    error "Failed to get example questions"
    exit 1
fi
echo ""

# Test 7: Ask Question to AI
echo "Test 7: Ask Question to AI"
info "POST /api/ask"
ASK_RESPONSE=$(curl -s -X POST "$BASE_URL/api/ask" \
    -H "Content-Type: application/json" \
    -d "{\"question\":\"What time is it?\",\"user_id\":\"$USER_ID\"}")

if echo "$ASK_RESPONSE" | grep -q "success"; then
    success "Successfully asked question to AI"
    RESPONSE_TEXT=$(echo "$ASK_RESPONSE" | jq -r '.data.response')
    info "AI Response: $RESPONSE_TEXT"
else
    error "Failed to ask question"
    echo "$ASK_RESPONSE"
    exit 1
fi
echo ""

# Test 8: Get Conversation History
echo "Test 8: Get Conversation History"
info "GET /api/conversation/$USER_ID"
if curl -s -f "$BASE_URL/api/conversation/$USER_ID" | grep -q "What time is it"; then
    success "Successfully retrieved conversation history"
else
    error "Failed to get conversation history"
    exit 1
fi
echo ""

# Test 9: Get User's Questions
echo "Test 9: Get User's Questions"
info "GET /users/$USER_ID/questions"
if curl -s -f "$BASE_URL/users/$USER_ID/questions" | grep -q "What time is it"; then
    success "Successfully retrieved user's questions"
else
    error "Failed to get user's questions"
    exit 1
fi
echo ""

# Test 10: Get All Questions
echo "Test 10: Get All Questions"
info "GET /questions"
if curl -s -f "$BASE_URL/questions" > /dev/null; then
    success "Successfully retrieved all questions"
else
    error "Failed to get all questions"
    exit 1
fi
echo ""

# Test 11: Get Assistant Status
echo "Test 11: Get Assistant Status"
info "GET /api/assistant/status"
if curl -s -f "$BASE_URL/api/assistant/status" | grep -q "initialized"; then
    success "Successfully retrieved assistant status"
else
    error "Failed to get assistant status"
    exit 1
fi
echo ""

# Test 12: Get Statistics
echo "Test 12: Get Statistics"
info "GET /stats"
if curl -s -f "$BASE_URL/stats" | grep -q "total_users"; then
    success "Successfully retrieved system statistics"
else
    error "Failed to get statistics"
    exit 1
fi
echo ""

# Test 13: Update User
echo "Test 13: Update User"
info "PUT /users/$USER_ID"
UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/users/$USER_ID" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"${TEST_USERNAME}_updated\"}")

if echo "$UPDATE_RESPONSE" | grep -q "success"; then
    success "Successfully updated user"
else
    error "Failed to update user"
    echo "$UPDATE_RESPONSE"
    exit 1
fi
echo ""

# Test 14: Delete User
echo "Test 14: Delete User"
info "DELETE /users/$USER_ID"
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/users/$USER_ID")

if echo "$DELETE_RESPONSE" | grep -q "success"; then
    success "Successfully deleted user"
else
    error "Failed to delete user"
    echo "$DELETE_RESPONSE"
    exit 1
fi
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}All tests passed successfully!${NC}"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Health endpoints: OK"
echo "  - User management: OK"
echo "  - Question management: OK"
echo "  - AI Assistant: OK"
echo "  - Statistics: OK"
echo ""
echo "Test user cleaned up: $TEST_USERNAME"
echo ""
