# TripVoice API

A Flask-based API that processes natural language trip requests and converts them to structured data format for further API calls.

## Features

- **AI-Powered Natural Language Processing** using Azure OpenAI (GPT-4o)
- **Hybrid Processing Strategy**: AI-first with intelligent rule-based fallback
- **Airport code extraction** (DEL, BOM, BLR, MAA, GOI, etc.)
- **Source and destination detection** from natural language
- **Missing field validation** with detailed error responses
- **Advanced text parsing** for complex travel requests
- **Relative date handling** (next monday, 3 days, tomorrow, etc.)
- **Duration calculation** for hotel checkout dates
- **Structured JSON output** for flight and hotel data
- **RESTful API endpoints** with comprehensive error handling

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

**Option A: Use the setup script (Recommended)**
```bash
python3 setup_env.py
```

**Option B: Manual setup**
Create a `.env` file in the root directory with the following variables:

```bash
# Azure OpenAI Configuration (All fields required)
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
AZURE_OPENAI_KEY=your_azure_openai_key_here
AZURE_OPENAI_DEPLOYMENT=your_deployment_name_here
AZURE_API_VERSION=your_api_version_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5001
```

**Important:** 
- Never commit your `.env` file to git. It's already included in `.gitignore`.
- All Azure OpenAI fields are required for the AI functionality to work.
- If you don't have Azure OpenAI credentials, the API will fall back to rule-based parsing.

### 3. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5001`

## API Endpoints

### Trip Planning

- **POST** `/api/trip/plan` - Convert natural language to structured trip data
- **GET** `/api/trip/health` - Health check for trip planning service
- **GET** `/api/trip/cities` - Get list of supported cities with their IDs, airport codes, and details

### Test Endpoints

- **GET** `/test/hello` - Simple hello message
- **POST** `/test/echo` - Echo back request data
- **GET** `/test/random` - Generate random data
- **GET** `/test/status/<status_code>` - Test different HTTP status codes
- **GET** `/test/headers` - Show request headers
- **GET** `/test/params` - Show query parameters

## Supported Cities

The API supports the following cities with their exact IDs, states, countries, and airport codes:

| City | City ID | State | Country | Type | Airport |
|------|---------|-------|---------|------|---------|
| Goa | 1138 | Goa | IN | STATE | GOI |
| Delhi | 700193 | Delhi | IN | CITY | DEL |
| Bangalore | 32550 | Karnataka | IN | CITY | BLR |
| Mumbai | 33719 | Maharashtra | IN | CITY | BOM |
| Hyderabad | 33897 | Telangana | IN | CITY | HYD |
| Chennai | 33070 | Tamil Nadu | IN | CITY | MAA |
| Jaipur | 33968 | Rajasthan | IN | CITY | JAI |
| Kolkata | 34600 | West Bengal | IN | CITY | CCU |
| Pune | 35943 | Maharashtra | IN | CITY | PNQ |
| Gurugram | 33752 | Haryana | IN | CITY | DEL |
| Udaipur | 36928 | Rajasthan | IN | CITY | UDR |
| Ahmedabad | 32136 | Gujarat | IN | CITY | AMD |
| Lucknow | 34849 | Uttar Pradesh | IN | CITY | LKO |
| Varanasi | 37069 | Uttar Pradesh | IN | CITY | VNS |
| Manali | 34981 | Himachal Pradesh | IN | CITY | KUU |
| Amritsar | 32257 | Punjab | IN | CITY | ATQ |
| Dubai | 100074 | Dubai | AE | CITY | DXB |
| Srinagar | 36623 | Jammu and Kashmir | IN | CITY | SXR |
| Noida | 35515 | Uttar Pradesh | IN | CITY | DEL |
| Kochi | 34571 | Kerala | IN | CITY | COK |

## AI Integration

This API uses **Azure OpenAI (GPT-4o)** for intelligent natural language processing with a **hybrid approach**:

### **AI-First Strategy:**
- **Primary**: Azure OpenAI processes natural language requests
- **Fallback**: Rule-based parsing when AI is unavailable
- **Benefits**: Better understanding of context, casual language, and complex requests

### **Key AI Capabilities:**
- **Smart City Detection**: Recognizes cities in casual language ("visit Mumbai", "going to Goa")
- **Context-Aware Parsing**: Understands travel intent and direction
- **Relative Date Processing**: Handles "next monday", "3 days", "tomorrow"
- **Duration Calculation**: Automatically calculates checkout dates based on trip duration

### **Example AI Processing:**
**Input**: "I want to visit Mumbai from delhi for 3 days with a budget of ₹5000 on next monday"

**AI Output**: 
```json
{
  "flight": {
    "from": "DEL",
    "to": "BOM", 
    "depart_date": "next monday",
    "adults": 2,
    "intl": "n"
  },
  "hotel": {
    "cityId": "33719",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "IN"
  }
}
```

**System Processing**: Converts "next monday" to "25/08/2025" and calculates checkout as "28/08/2025" (25/08 + 3 days)

## Usage Examples

### Trip Planning Request

**Endpoint:** `POST /api/trip/plan`

**Request Body:**
```json
{
    "text": "From Delhi to Goa for 2 adults next weekend"
}
```

**Success Response (200):**
```json
{
    "status": "success",
    "message": "Trip plan generated successfully",
    "input_text": "From Delhi to Goa for 2 adults next weekend",
    "trip_data": {
        "flight": {
            "from": "DEL",
            "to": "GOI",
            "depart_date": "22/08/2025",
            "adults": 2,
            "intl": "n"
        },
        "hotel": {
            "pageSize": 5,
            "pageNo": 1,
            "useCaseContext": "SRP_PAGE",
            "roomAllocations": [
                {
                    "adults": {
                        "count": 2,
                        "metadata": []
                    },
                    "children": {
                        "count": 0,
                        "metadata": []
                    }
                }
            ],
            "cityId": "1138",
            "city": "Goa",
            "state": "Goa",
            "country": "IN",
            "checkInDate": "22/08/2025",
            "checkOutDate": "23/08/2025",
            "version": "V2"
        }
    },
    "timestamp": "2025-01-20T10:30:00.000000"
}
```

**Insufficient Data Response (400):**
```json
{
    "status": "insufficient_data",
    "message": "Insufficient data provided. Please provide more details.",
    "input_text": "I want to travel somewhere nice",
    "trip_data": {
        "flight": {
            "from": "",
            "to": "",
            "depart_date": "22/08/2025",
            "adults": 2,
            "intl": "n"
        },
        "hotel": {
            "pageSize": 5,
            "pageNo": 1,
            "useCaseContext": "SRP_PAGE",
            "roomAllocations": [
                {
                    "adults": {
                        "count": 2,
                        "metadata": []
                    },
                    "children": {
                        "count": 0,
                        "metadata": []
                    }
                }
            ],
            "cityId": "",
            "city": "",
            "state": "",
            "country": "",
            "checkInDate": "22/08/2025",
            "checkOutDate": "23/08/2025",
            "version": "V2"
        }
    },
    "missing_fields": [
        "flight.from",
        "flight.to",
        "hotel.cityId",
        "hotel.city",
        "hotel.state"
    ],
    "timestamp": "2025-01-20T10:30:00.000000"
}
```

### Get Supported Cities

**Endpoint:** `GET /api/trip/cities`

**Response:**
```json
{
    "cities": [
        {
            "cityId": "1138",
            "city": "Goa",
            "state": "Goa",
            "country": "IN",
            "locationType": "STATE",
            "airport": "GOI"
        },
        {
            "cityId": "700193",
            "city": "Delhi",
            "state": "Delhi",
            "country": "IN",
            "locationType": "CITY",
            "airport": "DEL"
        }
    ],
    "count": 25,
    "timestamp": "2025-01-20T10:30:00.000000"
}
```

## Testing with Postman

### 1. Setup Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Create a new collection called "TripVoice API"

### 2. Test Trip Planning Endpoint

1. **Create a new request:**
   - Method: `POST`
   - URL: `http://localhost:5000/api/trip/plan`

2. **Set Headers:**
   - `Content-Type`: `application/json`

3. **Set Body (raw JSON):**
   ```json
   {
       "text": "From Delhi to Goa for 2 adults next weekend"
   }
   ```

4. **Send the request** and you should receive the structured trip data

### 3. Test Cities Endpoint

1. **Create a new request:**
   - Method: `GET`
   - URL: `http://localhost:5000/api/trip/cities`

2. **Send the request** to see all supported cities with airport codes

### 4. Test Health Endpoint

1. **Create a new request:**
   - Method: `GET`
   - URL: `http://localhost:5000/api/trip/health`

2. **Send the request** to check if the service is running

## Advanced Text Processing Features

The API intelligently processes natural language text to extract:

- **Source & Destination:** Automatically detects "from X to Y" patterns
- **Airport Codes:** Returns proper airport codes (DEL, BOM, BLR, MAA, GOI, etc.)
- **City Information:** Automatically detects cities from the supported list
- **Adult Count:** Extracts number of adults (defaults to 2 if not specified)
- **Dates:** Uses tomorrow and day after tomorrow as defaults
- **International Travel:** Automatically detects international destinations (e.g., Dubai)

## Response Status Types

- **`success`** (200): Complete trip data generated successfully
- **`insufficient_data`** (400): Missing required fields, returns partial data with missing field list
- **`error`** (400/500): Validation or server errors

## Default Values

- **Adults:** Defaults to 2 if not specified in the text
- **Dates:** Defaults to tomorrow and day after tomorrow if not specified
- **Version:** Always set to "V2"
- **Source:** Defaults to Delhi (DEL) if not specified
- **International:** Automatically detected based on destination country

## Error Handling

The API includes comprehensive error handling:
- **Input validation** with detailed error messages
- **Missing field detection** with specific field names
- **Partial data responses** when some information is available
- **Graceful fallbacks** for edge cases
- **HTTP status codes** for different error types
- **Structured error responses** for UI integration 