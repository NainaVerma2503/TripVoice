from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import requests
import json
import os
import re
from dateutil import parser

# Azure OpenAI configuration - Using your actual credentials
AZURE_OPENAI_ENDPOINT = "https://hackathon-openui-test.openai.azure.com/"
AZURE_OPENAI_KEY = "B4kxaCF6fe7KnBbRsDhk8EZZhvAz7MdVPXab3qJzZbahvpctLIT5JQQJ99BCAC77bzfXJ3w3AAABACOGTN88"
AZURE_OPENAI_DEPLOYMENT = "gpt-4o"
AZURE_API_VERSION = "2025-01-01-preview"



trip_bp = Blueprint('trip', __name__)

# City mapping data with airport codes
CITY_MAPPING = {
    "goa": {"cityId": "1138", "city": "Goa", "state": "Goa", "country": "IN", "locationType": "STATE", "airport": "GOI"},
    "delhi": {"cityId": "700193", "city": "Delhi", "state": "Delhi", "country": "IN", "locationType": "CITY", "airport": "DEL"},
    "new delhi": {"cityId": "700193", "city": "Delhi", "state": "Delhi", "country": "IN", "locationType": "CITY", "airport": "DEL"},
    "bangalore": {"cityId": "32550", "city": "Bangalore", "state": "Karnataka", "country": "IN", "locationType": "CITY", "airport": "BLR"},
    "bengaluru": {"cityId": "32550", "city": "Bangalore", "state": "Karnataka", "country": "IN", "locationType": "CITY", "airport": "BLR"},
    "mumbai": {"cityId": "33719", "city": "Mumbai", "state": "Maharashtra", "country": "IN", "locationType": "CITY", "airport": "BOM"},
    "bombay": {"cityId": "33719", "city": "Mumbai", "state": "Maharashtra", "country": "IN", "locationType": "CITY", "airport": "BOM"},
    "hyderabad": {"cityId": "33897", "city": "Hyderabad", "state": "Telangana", "country": "IN", "locationType": "CITY", "airport": "HYD"},
    "chennai": {"cityId": "33070", "city": "Chennai", "state": "Tamil Nadu", "country": "IN", "locationType": "CITY", "airport": "MAA"},
    "madras": {"cityId": "33070", "city": "Chennai", "state": "Tamil Nadu", "country": "IN", "locationType": "CITY", "airport": "MAA"},
    "jaipur": {"cityId": "33968", "city": "Jaipur", "state": "Rajasthan", "country": "IN", "locationType": "CITY", "airport": "JAI"},
    "kolkata": {"cityId": "34600", "city": "Kolkata", "state": "West Bengal", "country": "IN", "locationType": "CITY", "airport": "CCU"},
    "calcutta": {"cityId": "34600", "city": "Kolkata", "state": "West Bengal", "country": "IN", "locationType": "CITY", "airport": "CCU"},
    "pune": {"cityId": "35943", "city": "Pune", "state": "Maharashtra", "country": "IN", "locationType": "CITY", "airport": "PNQ"},
    "gurugram": {"cityId": "33752", "city": "Gurugram", "state": "Haryana", "country": "IN", "locationType": "CITY", "airport": "DEL"},
    "gurgaon": {"cityId": "33752", "city": "Gurugram", "state": "Haryana", "country": "IN", "locationType": "CITY", "airport": "DEL"},
    "udaipur": {"cityId": "36928", "city": "Udaipur", "state": "Rajasthan", "country": "IN", "locationType": "CITY", "airport": "UDR"},
    "ahmedabad": {"cityId": "32136", "city": "Ahmedabad", "state": "Gujarat", "country": "IN", "locationType": "CITY", "airport": "AMD"},
    "lucknow": {"cityId": "34849", "city": "Lucknow", "state": "Uttar Pradesh", "country": "IN", "locationType": "CITY", "airport": "LKO"},
    "varanasi": {"cityId": "37069", "city": "Varanasi", "state": "Uttar Pradesh", "country": "IN", "locationType": "CITY", "airport": "VNS"},
    "manali": {"cityId": "34981", "city": "Manali", "state": "Himachal Pradesh", "country": "IN", "locationType": "CITY", "airport": "KUU"},
    "amritsar": {"cityId": "32257", "city": "Amritsar", "state": "Punjab", "country": "IN", "locationType": "CITY", "airport": "ATQ"},
    "dubai": {"cityId": "100074", "city": "Dubai", "state": "Dubai", "country": "AE", "locationType": "CITY", "airport": "DXB"},
    "srinagar": {"cityId": "36623", "city": "Srinagar", "state": "Jammu and Kashmir", "country": "IN", "locationType": "CITY", "airport": "SXR"},
    "noida": {"cityId": "35515", "city": "Noida", "state": "Uttar Pradesh", "country": "IN", "locationType": "CITY", "airport": "DEL"},
    "kochi": {"cityId": "34571", "city": "Kochi", "state": "Kerala", "country": "IN", "locationType": "CITY", "airport": "COK"},
    "cochin": {"cityId": "34571", "city": "Kochi", "state": "Kerala", "country": "IN", "locationType": "CITY", "airport": "COK"}
}

def get_default_dates():
    """Get default dates (tomorrow and day after tomorrow)"""
    tomorrow = datetime.now() + timedelta(days=1)
    day_after = tomorrow + timedelta(days=1)
    
    return {
        'depart_date': tomorrow.strftime('%d/%m/%Y'),
        'check_in': tomorrow.strftime('%d/%m/%Y'),
        'check_out': day_after.strftime('%d/%m/%Y')
    }

def extract_city_info(text, city_type="destination"):
    """Extract city information from text"""
    text_lower = text.lower()
    
    for city_key, city_info in CITY_MAPPING.items():
        if city_key in text_lower:
            return city_info
    
    # Default to Mumbai if no city found
    return CITY_MAPPING["mumbai"]

def extract_source_and_destination(text):
    """Extract source and destination cities from text"""
    text_lower = text.lower()
    
    # Common source indicators
    source_indicators = [
        "from", "leaving", "departing", "starting from", "origin", "source"
    ]
    
    # Common destination indicators
    dest_indicators = [
        "to", "visiting", "going to", "destination", "arriving at", "headed to"
    ]
    
    source_city = None
    dest_city = None
    
    # Look for explicit source-destination patterns
    for source_ind in source_indicators:
        for dest_ind in dest_indicators:
            pattern = rf"{source_ind}\s+(\w+)\s+{dest_ind}\s+(\w+)"
            match = re.search(pattern, text_lower)
            if match:
                source_city = extract_city_info(match.group(1), "source")
                dest_city = extract_city_info(match.group(2), "destination")
                return source_city, dest_city
    
    # Look for "from X to Y" pattern
    from_to_pattern = r"from\s+(\w+)\s+to\s+(\w+)"
    match = re.search(from_to_pattern, text_lower)
    if match:
        source_city = extract_city_info(match.group(1), "source")
        dest_city = extract_city_info(match.group(2), "destination")
        return source_city, dest_city
    
    # Look for just source (e.g., "From Delhi")
    for source_ind in source_indicators:
        pattern = rf"{source_ind}\s+(\w+)"
        match = re.search(pattern, text_lower)
        if match:
            source_city = extract_city_info(match.group(1), "source")
            break
    
    # Look for just destination (e.g., "Goa", "to Goa")
    for dest_ind in dest_indicators:
        pattern = rf"{dest_ind}\s+(\w+)"
        match = re.search(pattern, text_lower)
        if match:
            dest_city = extract_city_info(match.group(1), "destination")
            break
    
    # If no destination indicator, look for city names directly
    if not dest_city:
        for city_key, city_info in CITY_MAPPING.items():
            if city_key in text_lower:
                dest_city = city_info
                break
    
    return source_city, dest_city

def extract_adults_count(text):
    """Extract number of adults from text"""
    text_lower = text.lower()
    
    # Look for specific patterns
    patterns = [
        r'(\d+)\s*adults?',
        r'(\d+)\s*people?',
        r'(\d+)\s*persons?',
        r'for\s*(\d+)\s*adults?',
        r'(\d+)\s*travelers?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            count = int(match.group(1))
            return min(count, 4)  # Cap at 4 adults
    
    # Default to 2 adults
    return 2

def parse_date_from_text(text, match_groups):
    """Parse actual date from text based on regex match groups"""
    try:
        text_lower = text.lower()
        
        # Month mapping
        month_map = {
            'january': 1, 'jan': 1,
            'february': 2, 'feb': 2,
            'march': 3, 'mar': 3,
            'april': 4, 'apr': 4,
            'may': 5,
            'june': 6, 'jun': 6,
            'july': 7, 'jul': 7,
            'august': 8, 'aug': 8,
            'september': 9, 'sep': 9,
            'october': 10, 'oct': 10,
            'november': 11, 'nov': 11,
            'december': 12, 'dec': 12
        }
        
        print(f"DEBUG: Parsing date from groups: {match_groups}")
        
        # Handle different date patterns
        if len(match_groups) == 3:
            # Format: "21st September 2025" or "September 21st 2025"
            if match_groups[0].isdigit() and match_groups[1].lower() in month_map:
                # "21st September 2025" format
                day = int(match_groups[0])
                month = month_map[match_groups[1].lower()]
                year = int(match_groups[2])
                print(f"DEBUG: Parsed as Day-Month-Year: {day}/{month}/{year}")
            elif match_groups[1].isdigit() and match_groups[0].lower() in month_map:
                # "September 21st 2025" format
                month = month_map[match_groups[0].lower()]
                day = int(match_groups[1])
                year = int(match_groups[2])
                print(f"DEBUG: Parsed as Month-Day-Year: {month}/{day}/{year}")
            else:
                print(f"DEBUG: Could not parse 3-group format")
                return None
        elif len(match_groups) == 2:
            # Format: "21st September" or "September 21st" (current year)
            current_year = datetime.now().year
            if match_groups[0].isdigit() and match_groups[1].lower() in month_map:
                # "21st September" format
                day = int(match_groups[0])
                month = month_map[match_groups[1].lower()]
                year = current_year
                print(f"DEBUG: Parsed as Day-Month (current year): {day}/{month}/{year}")
            elif match_groups[1].isdigit() and match_groups[0].lower() in month_map:
                # "September 21st" format
                month = month_map[match_groups[0].lower()]
                day = int(match_groups[1])
                year = current_year
                print(f"DEBUG: Parsed as Month-Day (current year): {month}/{day}/{year}")
            else:
                print(f"DEBUG: Could not parse 2-group format")
                return None
        else:
            print(f"DEBUG: Unexpected number of groups: {len(match_groups)}")
            return None
        
        print(f"DEBUG: Final parsed values - Day: {day}, Month: {month}, Year: {year}")
        
        # Create the date
        parsed_date = datetime(year, month, day)
        print(f"DEBUG: Created datetime object: {parsed_date}")
        
        # Check if date is in the past
        if parsed_date < datetime.now():
            print(f"DEBUG: Date {parsed_date} is in the past, using default")
            return None
        
        # Calculate check-in and check-out dates
        check_in = parsed_date
        check_out = parsed_date + timedelta(days=1)
        
        result = {
            'depart_date': parsed_date.strftime('%d/%m/%Y'),
            'check_in': check_in.strftime('%d/%m/%Y'),
            'check_out': check_out.strftime('%d/%m/%Y')
        }
        
        print(f"DEBUG: Final result: {result}")
        return result
        
    except Exception as e:
        print(f"DEBUG: Error parsing date: {str(e)}")
        return None

def extract_dates(text):
    """Extract dates from text or return None if not explicitly mentioned"""
    text_lower = text.lower()
    
    # Look for explicit date patterns
    date_patterns = [
        r'tomorrow',
        r'next\s+week',
        r'next\s+month',
        # Date formats like "21st September 2025", "25th December"
        r'(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})',
        r'(\d{1,2})(?:st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{4})',
        # Date formats like "September 21st 2025", "Dec 25th"
        r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})',
        r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})',
        # Standard date formats
        r'(\d{1,2})/(\d{1,2})/(\d{4})',
        r'(\d{1,2})-(\d{1,2})-(\d{4})',
        # Date formats like "21st September", "25th December" (current year)
        r'(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)',
        r'(\d{1,2})(?:st|nd|rd|th)?\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',
        # Date formats like "September 21st", "Dec 25th" (current year)
        r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(?:st|nd|rd|th)?',
        r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2})(?:st|nd|rd|th)?'
    ]
    
    # Check if any explicit date is mentioned
    for pattern in date_patterns:
        match = re.search(pattern, text_lower)
        if match:
            print(f"DEBUG: Date pattern matched: {pattern}")
            print(f"DEBUG: Date match groups: {match.groups()}")
            
            # Try to parse the actual date from text
            parsed_dates = parse_date_from_text(text, match.groups())
            if parsed_dates:
                print(f"DEBUG: Successfully parsed dates: {parsed_dates}")
                return parsed_dates
            else:
                print(f"DEBUG: Failed to parse dates, using defaults")
                # Fallback to default dates if parsing fails
                default_dates = get_default_dates()
                return default_dates
    
    # No explicit date mentioned, return None to indicate missing
    return None

def validate_trip_data(trip_data):
    """Validate trip data and return missing fields"""
    missing_fields = []
    
    # Check flight fields
    if not trip_data["flight"]["from"]:
        missing_fields.append("source")
    if not trip_data["flight"]["depart_date"]:
        missing_fields.append("departure_date")
    
    # Check destination - consolidate all destination-related fields into one "destination" field
    if not trip_data["flight"]["to"] or not trip_data["hotel"]["cityId"] or not trip_data["hotel"]["city"] or not trip_data["hotel"]["state"]:
        missing_fields.append("destination")
    
    # Don't check checkInDate and checkOutDate as missing - they'll be auto-calculated
    # from departure_date when it's available
    
    return missing_fields

def extract_trip_info_from_text(text):
    """Extract trip information from natural language text"""
    try:
        # Extract information using our parsing functions
        source_city, dest_city = extract_source_and_destination(text)
        adults_count = extract_adults_count(text)
        dates = extract_dates(text)
        
        # Check if we have sufficient data
        if not dest_city:
            return None, ["destination"]
        
        # Determine if international
        is_international = dest_city["country"] != "IN"
        
        # Create the structured response
        trip_data = {
            "flight": {
                "from": source_city["airport"] if source_city else "",
                "to": dest_city["airport"] if dest_city else "",
                "depart_date": dates['depart_date'] if dates else "",
                "adults": adults_count,
                "intl": "y" if is_international else "n"
            },
            "hotel": {
                "pageSize": 5,
                "pageNo": 1,
                "useCaseContext": "SRP_PAGE",
                "roomAllocations": [
                    {
                        "adults": {
                            "count": adults_count,
                            "metadata": []
                        },
                        "children": {
                            "count": 0,
                            "metadata": []
                        }
                    }
                ],
                "cityId": dest_city["cityId"] if dest_city else "",
                "city": dest_city["city"] if dest_city else "",
                "state": dest_city["state"] if dest_city else "",
                "country": dest_city["country"] if dest_city else "",
                "checkInDate": dates['check_in'] if dates else "",
                "checkOutDate": dates['check_out'] if dates else "",
                "version": "V2"
            }
        }
        
        # Validate the data
        missing_fields = validate_trip_data(trip_data)
        
        if missing_fields:
            return trip_data, missing_fields
        
        return trip_data, []
        
    except Exception as e:
        # Fallback response
        fallback_data = {
            "flight": {
                "from": "",
                "to": "",
                "depart_date": "",
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
                "checkInDate": "",
                "checkOutDate": "",
                "version": "V2"
            }
        }
        
        missing_fields = validate_trip_data(fallback_data)
        return fallback_data, missing_fields

def extract_trip_info_with_ai(text):
    """Use Azure OpenAI to extract trip information and return structured trip data"""
    try:
        print(f"DEBUG: Starting Azure OpenAI extraction for text: {text}")
        
        # Use direct HTTP requests to avoid SSL certificate issues
        url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={AZURE_API_VERSION}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AZURE_OPENAI_KEY}"
        }
        
        # Prepare the prompt to extract trip information and return structured data
        prompt = f"""Extract trip planning information from this text: "{text}" and return ONLY a JSON object in this exact format:

IMPORTANT: If the text says "From  to [city]" (with empty departure), leave the "from" field empty. Do NOT default to any city.

{{
  "flight": {{
    "from": "airport code or empty string if not mentioned",
    "to": "airport code or empty string if not mentioned", 
    "depart_date": "date in DD/MM/YYYY format or empty string if not mentioned",
    "adults": number of adults mentioned or 2 if not specified,
    "intl": "y" if international destination, "n" if domestic
  }},
  "hotel": {{
    "pageSize": 5,
    "pageNo": 1,
    "useCaseContext": "SRP_PAGE",
    "roomAllocations": [
      {{
        "adults": {{
          "count": number of adults mentioned or 2 if not specified,
          "metadata": []
        }},
        "children": {{
          "count": 0,
          "metadata": []
        }}
      }}
    ],
    "cityId": "city ID from mapping or empty string if not mentioned",
    "city": "city name or empty string if not mentioned",
    "state": "state name or empty string if not mentioned",
    "country": "country code (IN for India, AE for Dubai) or empty string if not mentioned",
    "checkInDate": "same as depart_date or empty string if not mentioned",
    "checkOutDate": "day after depart_date or empty string if not mentioned",
    "version": "V2"
  }}
}}

CRITICAL EXTRACTION RULES - BE VERY SMART:
1. **City Detection**: Look for ANY mention of cities, even in casual language like "visit Mumbai", "going to Goa", "trip to Bangalore", "visit [city]"
2. **Source Detection**: Look for "from [city]", "leaving [city]", "departing [city]", "starting from [city]"
3. **Date Detection**: Look for ANY date references like "3 days", "next week", "December", "15th March", "tomorrow", "next month", "next monday", "next tuesday", etc.
4. **Adults Detection**: Look for "2 adults", "family of 4", "3 people", "me and my friend" (count as 2)

**CRITICAL DESTINATION RULE**: If the text mentions "visit", "going to", "trip to", "travel to" but doesn't specify a city, you MUST detect this as missing destination information.

**CRITICAL DEPARTURE RULE**: If the text says "From  to [city]" or "From [empty] to [city]", leave the "from" field completely empty. Do NOT fill in any default city.

**CRITICAL DATE RULE**: When you see relative dates like "next monday", "3 days", "next week", return them as text strings like "next monday", "3 days", "next week". DO NOT try to calculate actual dates. Our system will handle the date calculation.

CITY MAPPING (ALWAYS USE THESE EXACT VALUES):
- **Delhi**: airport=DEL, cityId=700193, state=Delhi, country=IN
- **Mumbai**: airport=BOM, cityId=33719, state=Maharashtra, country=IN  
- **Bangalore**: airport=BLR, cityId=32550, state=Karnataka, country=IN
- **Chennai**: airport=MAA, cityId=33070, state=Tamil Nadu, country=IN
- **Kolkata**: airport=CCU, cityId=34600, state=West Bengal, country=IN
- **Jaipur**: airport=JAI, cityId=33968, state=Rajasthan, country=IN
- **Hyderabad**: airport=HYD, cityId=33897, state=Telangana, country=IN
- **Pune**: airport=PNQ, cityId=35943, state=Maharashtra, country=IN
- **Goa**: airport=GOI, cityId=1138, state=Goa, country=IN
- **Dubai**: airport=DXB, cityId=100074, state=Dubai, country=AE

SMART EXTRACTION TIPS:
- If text says "visit Mumbai", set "to": "BOM", "city": "Mumbai", "cityId": "33719", "state": "Maharashtra"
- If text says "visit Goa", set "to": "GOI", "city": "Goa", "cityId": "1138", "state": "Goa"
- If text says "visit Delhi", set "to": "DEL", "city": "Delhi", "cityId": "700193", "state": "Delhi"
- If text says "visit Bangalore", set "to": "BLR", "city": "Bangalore", "cityId": "32550", "state": "Karnataka"
- If text says "from Delhi", set "from": "DEL" 
- If text says "3 days", return "3 days" as depart_date (our system will calculate the actual date)
- If text says "next week", return "next week" as depart_date (our system will calculate the actual date)
- If text says "next monday", return "next monday" as depart_date (our system will calculate the actual date)
- If text says "next tuesday", return "next tuesday" as depart_date (our system will calculate the actual date)
- If text says "next wednesday", return "next wednesday" as depart_date (our system will calculate the actual date)
- If text says "next thursday", return "next thursday" as depart_date (our system will calculate the actual date)
- If text says "next friday", return "next friday" as depart_date (our system will calculate the actual date)
- If text says "next saturday", return "next saturday" as depart_date (our system will calculate the actual date)
- If text says "next sunday", return "next sunday" as depart_date (our system will calculate the actual date)
- If text says "tomorrow", return "tomorrow" as depart_date (our system will calculate the actual date)
- If text says "December", return "December" as depart_date (our system will calculate the actual date)
- If text says "family of 4", set adults=4
- If text says "me and my friend", set adults=2

**DESTINATION DETECTION**: If text says "I want to visit" but doesn't specify a city, leave destination fields empty and our system will mark "destination" as missing.

IMPORTANT: For relative dates, return the text exactly as mentioned (e.g., "next monday", "3 days"). Our system will handle the actual date calculation.

Return ONLY valid JSON, no additional text. Be very thorough in extraction!"""
        
        payload = {
            "messages": [
                {"role": "system", "content": "You are a travel planning assistant that extracts structured information from natural language text and returns it in the exact JSON format requested. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4096,
            "temperature": 0.1,
            "top_p": 1,
            "model": AZURE_OPENAI_DEPLOYMENT
        }
        
        print(f"DEBUG: Sending request to Azure OpenAI: {url}")
        
        # Make the HTTP request
        response = requests.post(url, headers=headers, json=payload, timeout=300)
        
        if response.status_code == 200:
            response_data = response.json()
            ai_response = response_data['choices'][0]['message']['content'].strip()
        print(f"DEBUG: Raw AI Response: {ai_response}")
        
        # Try to parse the JSON response
        try:
            # Remove any markdown formatting if present
            if ai_response.startswith('```json'):
                ai_response = ai_response.split('```json')[1]
            if ai_response.endswith('```'):
                ai_response = ai_response.rsplit('```', 1)[0]
            
            # Clean up the response
            ai_response = ai_response.strip()
            if ai_response.startswith('```'):
                ai_response = ai_response[3:]
            if ai_response.endswith('```'):
                ai_response = ai_response[:-3]
            
            print(f"DEBUG: Cleaned AI Response: {ai_response}")
            
            parsed_data = json.loads(ai_response.strip())
            print(f"DEBUG: Successfully parsed AI data: {parsed_data}")
            return parsed_data
            
        except json.JSONDecodeError as e:
            print(f"DEBUG: Failed to parse AI JSON: {e}")
            print(f"DEBUG: Problematic response: {ai_response}")
            return None
        else:
            print(f"DEBUG: Azure OpenAI API error - Status: {response.status_code}")
            print(f"DEBUG: Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"DEBUG: Azure OpenAI API error: {str(e)}")
        print(f"DEBUG: Error type: {type(e)}")
        return None

def extract_trip_info_hybrid(text):
    """Try AI first, fallback to rule-based extraction"""
    print(f"DEBUG: Attempting AI extraction for: {text}")
    
    # Try AI extraction first
    ai_result = extract_trip_info_with_ai(text)
    print(f"DEBUG: AI extraction result: {ai_result}")
    print(f"DEBUG: AI extraction result type: {type(ai_result)}")
    
    if ai_result:
        print(f"DEBUG: AI extraction successful: {ai_result}")
        
        # Convert relative dates to actual dates and handle duration
        ai_result = convert_relative_dates_with_duration(ai_result, text)
        print(f"DEBUG: After relative date conversion: {ai_result}")
        
        # AI already returns the correct format, just validate and return
        missing_fields = validate_trip_data(ai_result)
        if missing_fields:
            return ai_result, missing_fields
        return ai_result, []
    
    print(f"DEBUG: AI extraction failed, falling back to rule-based")
    # Fallback to rule-based extraction
    return extract_trip_info_from_text(text)

def convert_ai_result_to_trip_data(ai_result):
    """Convert AI extraction result to trip data format"""
    try:
        # Extract information from AI result
        source_city = ai_result.get("source_city")
        dest_city = ai_result.get("destination_city")
        travel_date = ai_result.get("travel_date")
        adults_count = ai_result.get("adults_count", 2)
        
        # Find city information
        source_city_info = None
        dest_city_info = None
        
        if source_city:
            for city_key, city_info in CITY_MAPPING.items():
                if city_key in source_city.lower():
                    source_city_info = city_info
                    break
        
        if dest_city:
            for city_key, city_info in CITY_MAPPING.items():
                if city_key in dest_city.lower():
                    dest_city_info = city_info
                    break
        
        # If no destination found, return error
        if not dest_city_info:
            return None, ["destination"]
        
        # Parse dates if provided
        dates = None
        if travel_date:
            # Use the existing date parsing logic
            dates = extract_dates_from_text(travel_date)
        
        # Determine if international
        is_international = dest_city_info["country"] != "IN"
        
        # Create trip data structure
        trip_data = {
            "flight": {
                "from": source_city_info["airport"] if source_city_info else "",
                "to": dest_city_info["airport"] if dest_city_info else "",
                "depart_date": dates['depart_date'] if dates else "",
                "adults": adults_count,
                "intl": "y" if is_international else "n"
            },
            "hotel": {
                "pageSize": 5,
                "pageNo": 1,
                "useCaseContext": "SRP_PAGE",
                "roomAllocations": [
                    {
                        "adults": {
                            "count": adults_count,
                            "metadata": []
                        },
                        "children": {
                            "count": 0,
                            "metadata": []
                        }
                    }
                ],
                "cityId": dest_city_info["cityId"] if dest_city_info else "",
                "city": dest_city_info["city"] if dest_city_info else "",
                "state": dest_city_info["state"] if dest_city_info else "",
                "country": dest_city_info["country"] if dest_city_info else "",
                "checkInDate": dates['check_in'] if dates else "",
                "checkOutDate": dates['check_out'] if dates else "",
                "version": "V2"
            }
        }
        
        # Validate the data
        missing_fields = validate_trip_data(trip_data)
        
        if missing_fields:
            return trip_data, missing_fields
        
        return trip_data, []
        
    except Exception as e:
        print(f"DEBUG: Error converting AI result: {str(e)}")
        return None, ["conversion_error"]

def extract_dates_from_text(text):
    """Extract dates from specific date text (used by AI conversion)"""
    # This function will use the existing date parsing logic
    # but can be called with specific date text from AI
    return extract_dates(text)

def convert_relative_dates(trip_data):
    """Convert relative dates in trip_data to actual dates"""
    try:
        if not trip_data or 'flight' not in trip_data:
            return trip_data
            
        depart_date = trip_data['flight'].get('depart_date', '')
        
        # If depart_date is empty or already a formatted date, return as is
        if not depart_date or '/' in depart_date:
            return trip_data
            
        # Convert relative dates to actual dates
        actual_dates = parse_relative_date(depart_date)
        if actual_dates:
            trip_data['flight']['depart_date'] = actual_dates['depart_date']
            if 'hotel' in trip_data:
                trip_data['hotel']['checkInDate'] = actual_dates['check_in']
                # Calculate checkout date based on duration mentioned in the original text
                # For now, we'll use the default +1 day, but this should be enhanced
                trip_data['hotel']['checkOutDate'] = actual_dates['check_out']
                
        return trip_data
    except Exception as e:
        print(f"DEBUG: Error converting relative dates: {str(e)}")
        return trip_data

def convert_relative_dates_with_duration(trip_data, original_text):
    """Convert relative dates in trip_data to actual dates and handle duration for checkout"""
    try:
        if not trip_data or 'flight' not in trip_data:
            return trip_data
            
        depart_date = trip_data['flight'].get('depart_date', '')
        
        # If depart_date is empty or already a formatted date, return as is
        if not depart_date or '/' in depart_date:
            return trip_data
            
        # Convert relative dates to actual dates
        actual_dates = parse_relative_date(depart_date)
        if actual_dates:
            trip_data['flight']['depart_date'] = actual_dates['depart_date']
            if 'hotel' in trip_data:
                trip_data['hotel']['checkInDate'] = actual_dates['check_in']
                
                # Calculate checkout date based on duration mentioned in original text
                duration_days = extract_duration_from_text(original_text)
                if duration_days and duration_days > 0:
                    # Calculate checkout date as departure date + duration days
                    depart_datetime = datetime.strptime(actual_dates['depart_date'], '%d/%m/%Y')
                    checkout_datetime = depart_datetime + timedelta(days=duration_days)
                    trip_data['hotel']['checkOutDate'] = checkout_datetime.strftime('%d/%m/%Y')
                else:
                    # Default to next day if no duration specified
                    trip_data['hotel']['checkOutDate'] = actual_dates['check_out']
                
        return trip_data
    except Exception as e:
        print(f"DEBUG: Error converting relative dates with duration: {str(e)}")
        return trip_data

def extract_duration_from_text(text):
    """Extract duration in days from text (e.g., '3 days', '5 days')"""
    try:
        import re
        # Look for patterns like "3 days", "5 days", "for 3 days", "trip for 3 days"
        patterns = [
            r'for\s+(\d+)\s+days?',
            r'(\d+)\s+days?',
            r'trip\s+for\s+(\d+)\s+days?',
            r'stay\s+for\s+(\d+)\s+days?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                days = int(match.group(1))
                print(f"DEBUG: Extracted duration: {days} days from text: '{text}'")
                return days
                
        return None
    except Exception as e:
        print(f"DEBUG: Error extracting duration: {str(e)}")
        return None

def parse_relative_date(relative_date_text):
    """Parse relative date text and return actual dates"""
    try:
        text = relative_date_text.lower().strip()
        today = datetime.now()
        
        if text == "tomorrow":
            depart_date = today + timedelta(days=1)
        elif text == "next monday":
            # Find next Monday
            days_ahead = 7 - today.weekday()  # Monday is 0
            if days_ahead <= 0:  # Today is Monday or later in the week
                days_ahead += 7
            depart_date = today + timedelta(days=days_ahead)
        elif text == "next tuesday":
            days_ahead = (8 - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            depart_date = today + timedelta(days=days_ahead)
        elif text == "next wednesday":
            days_ahead = (9 - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            depart_date = today + timedelta(days=days_ahead)
        elif text == "next thursday":
            days_ahead = (10 - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            depart_date = today + timedelta(days=days_ahead)
        elif text == "next friday":
            days_ahead = (11 - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            depart_date = today + timedelta(days=days_ahead)
        elif text == "next saturday":
            days_ahead = (12 - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            depart_date = today + timedelta(days=days_ahead)
        elif text == "next sunday":
            days_ahead = (13 - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            depart_date = today + timedelta(days=days_ahead)
        elif "days" in text:
            # Extract number of days
            import re
            match = re.search(r'(\d+)\s*days?', text)
            if match:
                days = int(match.group(1))
                depart_date = today + timedelta(days=days)
            else:
                return None
        elif text == "next week":
            depart_date = today + timedelta(days=7)
        else:
            return None
            
        # Calculate check-in and check-out dates
        check_in = depart_date
        check_out = depart_date + timedelta(days=1)
        
        return {
            'depart_date': depart_date.strftime('%d/%m/%Y'),
            'check_in': check_in.strftime('%d/%m/%Y'),
            'check_out': check_out.strftime('%d/%m/%Y')
        }
        
    except Exception as e:
        print(f"DEBUG: Error parsing relative date '{relative_date_text}': {str(e)}")
        return None

def fill_missing_trip_details(text, previous_trip_data):
    """Fill missing details in previous trip_data based on new text input using AI"""
    try:
        print(f"DEBUG: Using AI to fill missing trip details for: {text}")
        
        # Use AI extraction to get the complete information
        ai_result = extract_trip_info_with_ai(text)
        
        if ai_result:
            print(f"DEBUG: AI extraction successful: {ai_result}")
            
            # Create updated trip data by merging AI result with previous data
            updated_trip_data = previous_trip_data.copy()
            
            # Update flight information from AI result
            if ai_result.get("flight"):
                ai_flight = ai_result["flight"]
                
                # Only update departure city if AI found one (don't default to BOM)
                if ai_flight.get("from") and ai_flight["from"] != "":
                    print(f"DEBUG: AI found departure city: {ai_flight['from']}")
                    updated_trip_data["flight"]["from"] = ai_flight["from"]
                elif ai_flight.get("from") == "":
                    print(f"DEBUG: AI confirms departure city should remain empty")
                    updated_trip_data["flight"]["from"] = ""
                
                # Update other flight fields
                if ai_flight.get("to"):
                    updated_trip_data["flight"]["to"] = ai_flight["to"]
                if ai_flight.get("depart_date"):
                    updated_trip_data["flight"]["depart_date"] = ai_flight["depart_date"]
                if ai_flight.get("adults"):
                    updated_trip_data["flight"]["adults"] = ai_flight["adults"]
                if ai_flight.get("intl"):
                    updated_trip_data["flight"]["intl"] = ai_flight["intl"]
            
            # Update hotel information from AI result
            if ai_result.get("hotel"):
                ai_hotel = ai_result["hotel"]
                
                if ai_hotel.get("cityId"):
                    updated_trip_data["hotel"]["cityId"] = ai_hotel["cityId"]
                if ai_hotel.get("city"):
                    updated_trip_data["hotel"]["city"] = ai_hotel["city"]
                if ai_hotel.get("state"):
                    updated_trip_data["hotel"]["state"] = ai_hotel["state"]
                if ai_hotel.get("country"):
                    updated_trip_data["hotel"]["country"] = ai_hotel["country"]
                if ai_hotel.get("checkInDate"):
                    updated_trip_data["hotel"]["checkInDate"] = ai_hotel["checkInDate"]
                if ai_hotel.get("checkOutDate"):
                    updated_trip_data["hotel"]["checkOutDate"] = ai_hotel["checkOutDate"]
                
                # Update room allocations if adults count changed
                if ai_hotel.get("roomAllocations") and ai_hotel["roomAllocations"]:
                    adults_count = ai_hotel["roomAllocations"][0]["adults"]["count"]
                    updated_trip_data["hotel"]["roomAllocations"][0]["adults"]["count"] = adults_count
            
            # Convert relative dates to actual dates
            updated_trip_data = convert_relative_dates_with_duration(updated_trip_data, text)
            print(f"DEBUG: After relative date conversion: {updated_trip_data}")
            
            # Validate the updated data
            missing_fields = validate_trip_data(updated_trip_data)
            print(f"DEBUG: Missing fields after AI update: {missing_fields}")
            
            if missing_fields:
                return updated_trip_data, missing_fields
            return updated_trip_data, []
        
        else:
            print(f"DEBUG: AI extraction failed, falling back to rule-based")
            # Fallback to rule-based extraction only if AI fails completely
            return extract_trip_info_from_text(text)
        
    except Exception as e:
        print(f"DEBUG: Error in fill_missing_trip_details: {str(e)}")
        print(f"DEBUG: Error type: {type(e)}")
        # Return original data with error
        return previous_trip_data, ["server_error"]

def extract_user_interests_from_text(text):
    """
    Extract user interests from natural language text
    """
    text_lower = text.lower()
    interests = []
    
    # Define interest keywords
    interest_keywords = {
        "luxury": ["luxury", "premium", "high-end", "exclusive", "5-star", "five star"],
        "budget": ["budget", "cheap", "affordable", "economical", "low-cost"],
        "cultural": ["cultural", "heritage", "historical", "traditional", "monuments", "temples"],
        "adventure": ["adventure", "trekking", "hiking", "outdoor", "wildlife", "nature"],
        "food": ["food", "cuisine", "dining", "restaurant", "local food", "street food"],
        "shopping": ["shopping", "market", "mall", "retail", "buy"],
        "wellness": ["wellness", "spa", "relaxation", "yoga", "meditation", "health"],
        "beach": ["beach", "coastal", "seaside", "ocean", "waterfront"],
        "business": ["business", "corporate", "meeting", "conference", "work"],
        "family": ["family", "kids", "children", "family-friendly"],
        "romantic": ["romantic", "honeymoon", "couple", "romance", "intimate"],
        "nightlife": ["nightlife", "party", "clubs", "bars", "entertainment"]
    }
    
    # Check for each interest category
    for interest, keywords in interest_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                interests.append(interest)
                break
    
    # If no specific interests found, add general travel
    if not interests:
        interests = ["general travel"]
    
    return ", ".join(interests)


@trip_bp.route('/api/trip/plan', methods=['POST'])
def plan_trip():
    """AI-enhanced endpoint to plan a trip with better natural language understanding"""
    try:
        # Get the request data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'missing_fields': ['text'],
                'trip_data': None
            }), 400
        
        text = data['text']
        
        if not text or not text.strip():
            return jsonify({
                'missing_fields': ['text'],
                'trip_data': None
            }), 400
        
        # Check if user is providing previous trip_data to fill missing fields
        previous_trip_data = data.get('trip_data', None)
        
        if previous_trip_data:
            # User is filling in missing fields from previous response
            trip_data, missing_fields = fill_missing_trip_details(text, previous_trip_data)
        else:
            # First time request - try AI first, fallback to rule-based
            trip_data, missing_fields = extract_trip_info_hybrid(text)
        
        if missing_fields:
            # Return 400 with missing fields for UI to handle
            return jsonify({
                'missing_fields': missing_fields,
                'trip_data': trip_data
            }), 400
        
        # Success case - call search and package controllers
        try:
            # Step 1: Call Search Controller with trip data
            search_response = call_search_controller(trip_data["flight"], trip_data["hotel"])
            
            if not search_response or search_response.get('status') != 'success':
                return jsonify({
                    "error": "Search failed",
                    "search_error": search_response.get('error', 'Unknown error')
                }), 500
            
            # Step 2: Extract user interests from text or use defaults
            user_interests = extract_user_interests_from_text(text)
            budget_constraint = data.get('budget_constraint', 100000)
            num_packages = data.get('num_packages', 3)
            
            # Step 3: Call Package Controller with search results
            package_response = call_package_controller(
                search_response, 
                user_interests, 
                budget_constraint, 
                num_packages
            )
            
            if not package_response or package_response.get('status') != 'success':
                return jsonify({
                    "error": "Package creation failed",
                    "package_error": package_response.get('error', 'Unknown error'),
                    "search_summary": search_response.get('search_summary', {})
                }), 500
            
            # Step 4: Return just the packages list
            packages = package_response.get('packages', [])
            return jsonify({"packages": packages})
            
        except Exception as e:
            return jsonify({
                "error": f"Error in trip planning flow: {str(e)}"
            }), 500
        
    except Exception as e:
        return jsonify({
            'missing_fields': ['server_error'],
            'trip_data': None
        }), 500

@trip_bp.route('/api/trip/test-ai', methods=['POST'])
def test_ai_extraction():
    """Test endpoint for AI extraction functionality"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field'
            }), 400
        
        text = data['text']
        
        # Test AI extraction
        ai_result = extract_trip_info_with_ai(text)
        
        if ai_result:
            return jsonify({
                'success': True,
                'input_text': text,
                'ai_extraction': ai_result,
                'message': 'AI extraction successful'
            })
        else:
            return jsonify({
                'success': False,
                'input_text': text,
                'ai_extraction': None,
                'message': 'AI extraction failed'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Internal server error'
        }), 500

@trip_bp.route('/api/trip/sample', methods=['GET'])
def get_sample_response():
    """Get sample response in the exact format requested"""
    sample_response = {
        "flights": [
            {
                "airline": "IndiGo",
                "arrivalAirport": "BOM",
                "arrivalTerminal": "1",
                "arrivalTime": "2025-08-22T15:05:00.000+05:30",
                "departureAirport": "DEL",
                "departureTerminal": "1D",
                "departureTime": "2025-08-22T13:25:00.000+05:30",
                "flightNumber": "6E-129",
                "id": "sample_flight_001",
                "legs": [
                    {
                        "arrivalTerminal": "1",
                        "departureTerminal": "1D",
                        "flightNumber": "6E-129"
                    }
                ],
                "stopDetails": "Direct flight",
                "stops": 0,
                "totalDuration": "1h 40m"
            }
        ],
        "hotels": [
            {
                "amenities": [
                    "WiFi",
                    "Pool",
                    "Spa",
                    "Restaurant"
                ],
                "id": "sample_hotel_001",
                "location": {
                    "address": "Apollo Bunder, Mumbai",
                    "area": "Colaba",
                    "city": "Mumbai"
                },
                "name": "Taj Palace Hotel",
                "price": {
                    "amount": 15000,
                    "currency": "INR"
                },
                "rating": 5
            }
        ],
        "search_summary": {
            "adults": 1,
            "departure_date": "22/08/2025",
            "from": "DEL",
            "to": "BOM",
            "total_flights_found": 1,
            "total_hotels_found": 1
        },
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(sample_response)

@trip_bp.route('/api/trip/health', methods=['GET'])
def trip_health():
    """Health check for trip planning service"""
    return jsonify({
        'status': 'healthy',
        'service': 'Trip Planning',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/api/trip/plan',
            '/api/trip/health',
            '/api/trip/cities',
            '/api/trip/test-ai',
            '/api/trip/sample'
        ]
    })

@trip_bp.route('/api/trip/cities', methods=['GET'])
def get_cities():
    """Get list of supported cities"""
    return jsonify({
        'cities': list(CITY_MAPPING.values()),
        'count': len(CITY_MAPPING),
        'timestamp': datetime.now().isoformat()
    }) 

@trip_bp.route('/api/trip/create-packages', methods=['POST'])
def create_trip_packages():
    """
    Orchestrate the complete flow: Search → Package Creation → Response
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract user preferences and search criteria
        user_interests = data.get('user_interests', '')
        budget_constraint = data.get('budget_constraint', 100000)
        num_packages = data.get('num_packages', 3)
        
        # Extract search criteria
        flight_data = data.get('flight', {})
        hotel_data = data.get('hotel', {})
        
        if not flight_data or not hotel_data:
            return jsonify({"error": "Both flight and hotel search criteria required"}), 400
        
        # Step 1: Call Search Controller
        search_response = call_search_controller(flight_data, hotel_data)
        
        if not search_response or search_response.get('status') != 'success':
            return jsonify({
                "error": "Search failed",
                "search_error": search_response.get('error', 'Unknown error')
            }), 500
        
        # Step 2: Call Package Controller with search results
        package_response = call_package_controller(
            search_response, 
            user_interests, 
            budget_constraint, 
            num_packages
        )
        
        if not package_response or package_response.get('status') != 'success':
            return jsonify({
                "error": "Package creation failed",
                "package_error": package_response.get('error', 'Unknown error')
            }), 500
        
        # Step 3: Return final response
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "search_summary": search_response.get('search_summary', {}),
            "packages": package_response.get('packages', []),
            "package_count": package_response.get('package_count', 0),
            "user_interests": user_interests,
            "budget_constraint": budget_constraint,
            "flow": "Trip Controller → Search Controller → Package Controller"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }), 500

def call_search_controller(flight_data, hotel_data):
    """
    Call the search controller to get flight and hotel data
    """
    try:
        # Prepare search request
        search_request = {
            "flight": flight_data,
            "hotel": hotel_data
        }
        
        # Use HTTP call to search controller
        search_url = "http://localhost:6000/api/search"
        response = requests.post(search_url, json=search_request, timeout=300)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "error": f"Search API failed: {response.status_code}"}
        
    except Exception as e:
        print(f"Error calling search controller: {e}")
        return {"status": "error", "error": str(e)}

def call_package_controller(search_response, user_interests, budget_constraint, num_packages):
    """
    Call the package controller to create packages from search results
    """
    try:
        # Prepare package request
        package_request = {
            "search_response": {
                "flights": search_response.get('flights', []),
                "hotels": search_response.get('hotels', [])
            },
            "user_interests": user_interests,
            "budget_constraint": budget_constraint,
            "num_packages": num_packages
        }
        
        # Use HTTP call to package controller
        package_url = "http://localhost:6000/api/package/create-from-search"
        response = requests.post(package_url, json=package_request, timeout=300)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "error": f"Package API failed: {response.status_code}"}
        
    except Exception as e:
        print(f"Error calling package controller: {e}")
        return {"status": "error", "error": str(e)} 

