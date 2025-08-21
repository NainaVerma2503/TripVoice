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

### Search and Package APIs
- **`/api/search`** - Search for flights and hotels using ClearTrip APIs
- **`/api/package/create`** - Create travel packages using GenAI based on flight/hotel data
- **`/api/package/create-from-search`** - Create travel packages from search parameters using GenAI

### Image APIs
- **`/images/<category>/<filename>`** - Serve local images from the project
- **`/api/images/list`** - List all available images in the project

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

### Search API Testing
```bash
# Test search API
python3 test_final_api.py

# Test package creation APIs
python3 test_package_creation.py

# Create sample images
python3 create_sample_images.py
```

## Project Structure

```
TripVoice/
├── app.py                 # Main Flask application
├── controllers/           # Controller modules
│   ├── __init__.py
│   ├── main_controller.py # Main controller with test endpoints
│   ├── search_controller.py # Search API for flights and hotels
│   └── package_controller.py # Package creation with GenAI
├── tests/                 # Testing utilities
│   ├── __init__.py
│   └── test_controller.py # Automated testing script
├── test_final_api.py      # Search API testing script
├── test_package_creation.py # Package creation testing script
├── create_sample_images.py # Script to create sample images
├── images/                # Image assets directory
│   ├── packages/         # Package images
│   ├── flights/          # Flight and aircraft images
│   ├── hotels/           # Hotel images
│   ├── amenities/        # Amenity icons
│   └── airlines/         # Airline logos
├── requirements.txt       # Python dependencies
└── README.md             # This file

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

## Package Creation with GenAI

The service includes AI-powered travel package creation using Azure OpenAI GPT-4. The package creation APIs analyze flight and hotel data along with user preferences to generate personalized travel packages.

### Features:
- **Intelligent Package Matching**: AI analyzes user preferences and available options
- **Budget Optimization**: Creates packages based on budget constraints
- **Interest-Based Recommendations**: Tailors packages to user interests (adventure, cultural, luxury, etc.)
- **Multiple Package Types**: Budget, Mid-range, Luxury, and Premium packages
- **Comprehensive Details**: Includes flight details, hotel information, pricing breakdown, and recommendations

### User Preferences Supported:
- **Budget**: budget, medium, luxury, premium
- **Interests**: adventure, cultural, food, shopping, wellness, business, family
- **Travel Style**: leisure, business, adventure, romantic
- **Duration**: 1-3 days, 3-5 days, 5-7 days, 7+ days
- **Group Size**: Solo, couple, family, group
- **Preferred Airlines**: Specific airline preferences
- **Preferred Hotel Chains**: Specific hotel brand preferences
- **Must-Have Amenities**: Essential amenities required
- **Optional Amenities**: Nice-to-have amenities

### Package Response Structure:
```json
{
  "status": "success",
  "timestamp": "2024-01-XX...",
  "packages": [
    {
      "package_id": "package_001",
      "package_name": "Luxury Mumbai Getaway",
      "package_type": "Luxury",
      "target_audience": "Couples, Business travelers",
      "description": "A premium travel experience...",
      "duration": "3-5 days",
      "flight": {
        "flight_id": "flight_001",
        "airline": "Vistara",
        "flight_number": "UK-825",
        "departure": "DEL",
        "arrival": "BOM",
        "departure_time": "2025-08-22T16:00:00.000+05:30",
        "arrival_time": "2025-08-22T18:20:00.000+05:30",
        "duration": "2h 20m",
        "price": 8500
      },
      "hotel": {
        "hotel_id": "hotel_001",
        "name": "Taj Palace Hotel",
        "location": "Colaba, Mumbai",
        "rating": 5,
        "amenities": ["WiFi", "Pool", "Spa", "Restaurant"],
        "price_per_night": 15000
      },
      "package_highlights": [
        "Direct flight with premium airline",
        "5-star luxury hotel in prime location",
        "Spa and wellness facilities",
        "Fine dining experience"
      ],
      "total_package_price": 85000,
      "price_breakdown": {
        "flight": 8500,
        "hotel": 60000,
        "taxes": 16500
      },
      "recommendation_reason": "Perfect for luxury travelers seeking premium experience",
      "included_amenities": ["Flight", "Hotel", "Airport Transfer", "Welcome Drink"],
      "optional_addons": ["Spa Package", "City Tour", "Dinner at Fine Restaurant"]
    }
  ],
  "package_count": 1
}
``` 