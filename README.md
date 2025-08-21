# TripVoice Flask Service

A Flask API service with organized controllers and comprehensive testing endpoints.

## Setup

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the service:**
   ```bash
   python app.py
   ```

The service will start on `http://localhost:5000`

## API Endpoints

### Basic Endpoints
- **`/`** - Home endpoint with service information
- **`/health`** - Health check endpoint
- **`/api/status`** - API status and available endpoints

### Controller Test Endpoints
- **`/test/hello`** - Simple hello message from controller
- **`/test/random`** - Generates random numbers and floats
- **`/test/echo`** - POST endpoint that echoes back request data
- **`/test/status/<status_code>`** - Test different HTTP status codes (200, 201, 400, 401, 404, 500)
- **`/test/headers`** - Shows request headers received
- **`/test/params`** - Shows query parameters received

## Testing the Service

### Quick Test
```bash
# Test basic endpoints
curl http://localhost:5000/health
curl http://localhost:5000/test/hello

# Test POST endpoint
curl -X POST -H "Content-Type: application/json" \
  -d '{"message": "Hello Controller!", "user": "Tester"}' \
  http://localhost:5000/test/echo

# Test with query parameters
curl "http://localhost:5000/test/params?name=test&value=123"
```

### Comprehensive Testing
Run the automated test script:
```bash
python tests/test_controller.py
```

This will test all endpoints and show which ones are working correctly.

## Project Structure

```
TripVoice/
├── app.py                 # Main Flask application
├── controllers/           # Controller modules
│   ├── __init__.py
│   └── main_controller.py # Main controller with test endpoints
├── tests/                 # Testing utilities
│   ├── __init__.py
│   └── test_controller.py # Automated testing script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Expected Responses

### Health Check
```json
{
  "status": "healthy",
  "service": "TripVoice",
  "timestamp": "2024-01-XX...",
  "version": "1.0.0"
}
```

### Controller Hello
```json
{
  "message": "Hello from TripVoice Controller!",
  "endpoint": "/test/hello",
  "timestamp": "2024-01-XX..."
}
```

### Random Data
```json
{
  "random_number": 42,
  "random_float": 0.1234,
  "message": "Random data generated successfully",
  "timestamp": "2024-01-XX..."
}
``` 