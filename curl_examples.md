# Package Creation API - cURL Examples

## API Endpoint
```
POST http://localhost:6000/api/package/create-from-search
```

## Example 1: Beach Lover Package

```bash
curl -X POST "http://localhost:6000/api/package/create-from-search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_response": {
      "packageName": "One-Way Luxury Arrival: The St. Regis Goa",
      "packageType": "ONE_WAY_LUXURY",
      "totalPrice": 62800,
      "currency": "INR",
      "duration": "4 Nights / 5 Days Hotel Stay",
      "description": "This package arranges your luxury one-way arrival to Goa and a magnificent 4-night stay at the St. Regis Resort.",
      "flightDetails": {
        "airline": "Air India",
        "flightNumber": "AI 2803 / AI 2657",
        "price": {
          "value": 15000,
          "currency": "INR"
        },
        "departureAirportCode": "DEL",
        "departureCity": "New Delhi",
        "departureDateTime": "2025-08-22T10:00:00",
        "arrivalAirportCode": "GOI",
        "arrivalCity": "Goa",
        "arrivalDateTime": "2025-08-22T12:30:00",
        "stops": "1 stop",
        "duration": "2h 30m"
      },
      "hotelDetails": {
        "name": "The St. Regis Goa Resort",
        "starRating": 5,
        "price": "13000",
        "address": "Mobor, Cavelossim, Goa, 403731, India",
        "city": "Mobor Beach, Goa",
        "amenities": [
          "Private Beach Access",
          "24-hour St. Regis Butler Service",
          "Spa and Wellness Center",
          "Championship Golf Course"
        ],
        "images": [
          "https://example-cdn.com/cms/6554/6554918/images/xr-goixr-goixr-aerial-resort-hero-26597_Classic-Hor_T.jpg"
        ]
      }
    },
    "user_interests": "beach, water sports, relaxation, sunset views",
    "budget_constraint": 80000,
    "num_packages": 3
  }'
```

## Example 2: Cultural Heritage Package

```bash
curl -X POST "http://localhost:6000/api/package/create-from-search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_response": {
      "packageName": "Delhi Heritage Explorer",
      "packageType": "HERITAGE_EXPLORER",
      "totalPrice": 45000,
      "currency": "INR",
      "duration": "3 Nights / 4 Days",
      "description": "Explore the rich cultural heritage of Delhi with this comprehensive package.",
      "flightDetails": {
        "airline": "IndiGo",
        "flightNumber": "6E-129",
        "price": {
          "value": 8000,
          "currency": "INR"
        },
        "departureAirportCode": "BOM",
        "departureCity": "Mumbai",
        "departureDateTime": "2025-08-22T08:00:00",
        "arrivalAirportCode": "DEL",
        "arrivalCity": "New Delhi",
        "arrivalDateTime": "2025-08-22T10:15:00",
        "stops": "Direct",
        "duration": "2h 15m"
      },
      "hotelDetails": {
        "name": "The Leela Palace New Delhi",
        "starRating": 5,
        "price": "15000",
        "address": "Diplomatic Enclave, New Delhi, India",
        "city": "New Delhi",
        "amenities": [
          "WiFi",
          "Pool",
          "Spa",
          "Restaurant",
          "Concierge"
        ],
        "images": [
          "https://example.com/leela-delhi-1.jpg"
        ]
      }
    },
    "user_interests": "culture, heritage, traditional food, historical monuments",
    "budget_constraint": 60000,
    "num_packages": 2
  }'
```

## Example 3: Adventure Package

```bash
curl -X POST "http://localhost:6000/api/package/create-from-search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_response": {
      "packageName": "Himalayan Adventure Package",
      "packageType": "ADVENTURE_EXPLORER",
      "totalPrice": 55000,
      "currency": "INR",
      "duration": "5 Nights / 6 Days",
      "description": "Experience the thrill of Himalayan adventures with this action-packed package.",
      "flightDetails": {
        "airline": "Vistara",
        "flightNumber": "UK-825",
        "price": {
          "value": 12000,
          "currency": "INR"
        },
        "departureAirportCode": "DEL",
        "departureCity": "New Delhi",
        "departureDateTime": "2025-08-22T06:00:00",
        "arrivalAirportCode": "DED",
        "arrivalCity": "Dehradun",
        "arrivalDateTime": "2025-08-22T07:30:00",
        "stops": "Direct",
        "duration": "1h 30m"
      },
      "hotelDetails": {
        "name": "Adventure Lodge Rishikesh",
        "starRating": 4,
        "price": "8000",
        "address": "Rishikesh, Uttarakhand, India",
        "city": "Rishikesh",
        "amenities": [
          "Adventure Equipment",
          "Guided Tours",
          "Camping Facilities",
          "River Rafting"
        ],
        "images": [
          "https://example.com/adventure-lodge-1.jpg"
        ]
      }
    },
    "user_interests": "adventure, trekking, river rafting, wildlife, camping",
    "budget_constraint": 100000,
    "num_packages": 3
  }'
```

## Example 4: Food & Shopping Package

```bash
curl -X POST "http://localhost:6000/api/package/create-from-search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_response": {
      "packageName": "Mumbai Food & Shopping Extravaganza",
      "packageType": "URBAN_EXPLORER",
      "totalPrice": 35000,
      "currency": "INR",
      "duration": "3 Nights / 4 Days",
      "description": "Indulge in the best of Mumbai\'s food scene and shopping districts.",
      "flightDetails": {
        "airline": "Air India",
        "flightNumber": "AI-101",
        "price": {
          "value": 7000,
          "currency": "INR"
        },
        "departureAirportCode": "DEL",
        "departureCity": "New Delhi",
        "departureDateTime": "2025-08-22T09:00:00",
        "arrivalAirportCode": "BOM",
        "arrivalCity": "Mumbai",
        "arrivalDateTime": "2025-08-22T11:15:00",
        "stops": "Direct",
        "duration": "2h 15m"
      },
      "hotelDetails": {
        "name": "Taj Lands End",
        "starRating": 5,
        "price": "12000",
        "address": "Bandra West, Mumbai, Maharashtra, India",
        "city": "Mumbai",
        "amenities": [
          "WiFi",
          "Pool",
          "Spa",
          "Multiple Restaurants",
          "Shopping Arcade"
        ],
        "images": [
          "https://example.com/taj-lands-end-1.jpg"
        ]
      }
    },
    "user_interests": "food, shopping, street food, local markets, nightlife",
    "budget_constraint": 50000,
    "num_packages": 2
  }'
```

## Response Format

The API returns a JSON response with the following structure:

```json
{
  "status": "success",
  "packages": [
    {
      "packageName": "Package Name",
      "packageType": "BUDGET/MID_RANGE/LUXURY/PREMIUM",
      "totalPrice": 45000,
      "currency": "INR",
      "duration": "3 Nights / 4 Days",
      "description": "Package description",
      "flightDetails": {
        "airline": "Airline name",
        "flightNumber": "Flight number",
        "price": {
          "value": 8000,
          "currency": "INR"
        },
        "departureAirportCode": "DEL",
        "departureCity": "New Delhi",
        "departureDateTime": "2025-08-22T10:00:00",
        "arrivalAirportCode": "BOM",
        "arrivalCity": "Mumbai",
        "arrivalDateTime": "2025-08-22T12:15:00",
        "stops": "Direct",
        "duration": "2h 15m"
      },
      "hotelDetails": {
        "name": "Hotel name",
        "starRating": 5,
        "price": "12000",
        "address": "Hotel address",
        "city": "City name",
        "amenities": ["WiFi", "Pool", "Spa"],
        "images": ["image_url1", "image_url2"]
      },
      "suggestedItinerary": [
        {
          "day": 1,
          "title": "Day title",
          "activities": ["activity1", "activity2", "activity3"]
        }
      ],
      "popularAttractions": ["attraction1", "attraction2", "attraction3"],
      "whyThisPackage": "Explanation of why this package matches user interests",
      "budgetBreakdown": {
        "flight": 8000,
        "hotel": 12000,
        "activities": 5000,
        "taxes": 2500,
        "total": 27500
      }
    }
  ],
  "package_count": 3,
  "user_interests": "beach, water sports, relaxation",
  "budget_constraint": 80000,
  "timestamp": "2025-08-21T18:30:00.123456"
}
```

## Parameters

- `search_response`: The search response data containing flight and hotel details
- `user_interests`: String describing user interests (e.g., "beach, culture, adventure")
- `budget_constraint`: Maximum budget in INR (default: 100000)
- `num_packages`: Number of packages to generate (default: 3)

## Notes

1. The API will try to use OpenAI to generate personalized packages
2. If OpenAI fails, it will create fallback packages based on user interests
3. All packages will be within the specified budget constraint
4. Packages include detailed itineraries and attractions based on user interests
5. The API automatically adjusts pricing to fit within budget constraints
