#!/usr/bin/env python3
"""
Simple test script for TripVoice Trip Planning API
Run this to test the API without Postman
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/trip/health")
        if response.status_code == 200:
            print("✅ Health endpoint working!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
        print()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running!")
        print()

def test_cities_endpoint():
    """Test the cities endpoint"""
    print("🔍 Testing cities endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/trip/cities")
        if response.status_code == 200:
            print("✅ Cities endpoint working!")
            data = response.json()
            print(f"Total cities supported: {data['count']}")
            print("Sample cities with airport codes:")
            for city in data['cities'][:5]:  # Show first 5 cities
                print(f"  - {city['city']}, {city['state']} (ID: {city['cityId']}, Airport: {city['airport']})")
        else:
            print(f"❌ Cities endpoint failed with status {response.status_code}")
        print()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running!")
        print()

def test_trip_planning():
    """Test the trip planning endpoint with sample text"""
    print("🔍 Testing trip planning endpoint...")
    
    # Sample trip requests
    test_cases = [
        "From Delhi to Goa for 2 adults next weekend",
        "From Mumbai to Bangalore for 3 adults next week",
        "From Kolkata to Jaipur for 4 people",
        "From Delhi to Dubai with 2 adults",
        "From Chennai to Hyderabad next month"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {text}")
        
        try:
            payload = {"text": text}
            response = requests.post(
                f"{BASE_URL}/api/trip/plan",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print("✅ Success!")
                # Response is now directly the trip_data
                trip_data = response.json()
                
                # Show flight details
                flight = trip_data['flight']
                print(f"✈️  Flight: {flight['from']} → {flight['to']}")
                print(f"   Date: {flight['depart_date']}, Adults: {flight['adults']}, International: {flight['intl']}")
                
                # Show hotel details
                hotel = trip_data['hotel']
                print(f"🏨 Hotel: {hotel['city']}, {hotel['state']}")
                print(f"   City ID: {hotel['cityId']}, Country: {hotel['country']}")
                print(f"   Check-in: {hotel['checkInDate']}, Check-out: {hotel['checkOutDate']}")
                print(f"   Adults: {hotel['roomAllocations'][0]['adults']['count']}")
                
            elif response.status_code == 400:
                data = response.json()
                if 'missing_fields' in data:
                    print("⚠️  Insufficient Data (Expected 400)")
                    print(f"Missing fields: {data['missing_fields']}")
                    if data['trip_data']:
                        print(f"Partial data available: {data['trip_data']['hotel']['city']}")
                    else:
                        print("No partial data available")
                else:
                    print(f"❌ Unexpected error response: {data}")
            else:
                print(f"❌ Failed with status {response.status_code}")
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API. Make sure the server is running!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        time.sleep(1)  # Small delay between requests

def test_missing_source_scenarios():
    """Test scenarios where source is missing (should return 400)"""
    print("\n🔍 Testing missing source scenarios...")
    
    missing_source_cases = [
        "I want to visit Mumbai for 3 days with a budget of ₹5000",
        "Goa trip for 2 adults",
        "Weekend vacation to Bangalore",
        "Need a hotel in Chennai for tomorrow",
        "Travel to Jaipur next week"
    ]
    
    for i, text in enumerate(missing_source_cases, 1):
        print(f"\n📝 Missing Source Test {i}: {text}")
        
        try:
            payload = {"text": text}
            response = requests.post(
                f"{BASE_URL}/api/trip/plan",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 400:
                data = response.json()
                if 'missing_fields' in data:
                    print("✅ Correctly returned 400 for missing data")
                    print(f"Missing fields: {data['missing_fields']}")
                    
                    # Check specific missing fields
                    missing_fields = data['missing_fields']
                    if 'source' in missing_fields:
                        print("   ✓ Source field correctly identified as missing")
                    if 'departure_date' in missing_fields:
                        print("   ✓ Departure date correctly identified as missing")
                    # Note: check_in_date and check_out_date are no longer missing fields
                    # as they're auto-calculated from departure_date
                    
                    # Show what data was extracted
                    if data['trip_data']:
                        trip_data = data['trip_data']
                        print(f"   Extracted destination: {trip_data['hotel']['city']}")
                        print(f"   Extracted adults: {trip_data['flight']['adults']}")
                        print(f"   Flight from: '{trip_data['flight']['from']}' (should be empty)")
                        print(f"   Flight to: '{trip_data['flight']['to']}'")
                        print(f"   Departure date: '{trip_data['flight']['depart_date']}' (should be empty if no date mentioned)")
                        print(f"   Check-in date: '{trip_data['hotel']['checkInDate']}' (auto-calculated when departure date is set)")
                        print(f"   Check-out date: '{trip_data['hotel']['checkOutDate']}' (auto-calculated when departure date is set)")
                    else:
                        print("   No partial data available")
                else:
                    print(f"❌ Unexpected error response: {data}")
            else:
                print(f"❌ Expected 400, got {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to API")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        time.sleep(0.5)

def test_date_extraction():
    """Test date extraction with and without explicit dates"""
    print("\n🔍 Testing date extraction...")
    
    date_test_cases = [
        "From Delhi to Mumbai tomorrow",
        "From Bangalore to Goa next week",
        "From Kolkata to Chennai next month",
        "From Delhi to Jaipur on 25th December",
        "From Mumbai to Bangalore on 15/12/2025",
        "From Chennai to Hyderabad on 20-Aug-2025"
    ]
    
    for i, text in enumerate(date_test_cases, 1):
        print(f"\n📅 Date Test {i}: {text}")
        
        try:
            payload = {"text": text}
            response = requests.post(
                f"{BASE_URL}/api/trip/plan",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                # Response is now directly the trip_data
                trip_data = response.json()
                flight = trip_data['flight']
                print(f"   ✅ Success - From: {flight['from']} → To: {flight['to']}")
                print(f"   Departure date: {flight['depart_date']}")
            elif response.status_code == 400:
                data = response.json()
                if 'missing_fields' in data:
                    print(f"   ⚠️  Insufficient data - Missing: {data['missing_fields']}")
                else:
                    print(f"   ❌ Unexpected error response: {data}")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Cannot connect to API")
            break
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        time.sleep(0.5)

def test_error_cases():
    """Test error handling"""
    print("\n🔍 Testing error cases...")
    
    # Test with missing text
    print("📝 Testing missing text field...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/trip/plan",
            json={},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Correctly handled missing text field")
            print(f"Missing fields: {data.get('missing_fields', [])}")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
    
    # Test with empty text
    print("\n📝 Testing empty text...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/trip/plan",
            json={"text": ""},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Correctly handled empty text")
            print(f"Missing fields: {data.get('missing_fields', [])}")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
    
    # Test with insufficient data (no city mentioned)
    print("\n📝 Testing insufficient data (no city)...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/trip/plan",
            json={"text": "I want to travel somewhere nice"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            data = response.json()
            if 'missing_fields' in data:
                print("✅ Correctly handled insufficient data")
                print(f"Missing fields: {data['missing_fields']}")
            else:
                print(f"❌ Unexpected error response: {data}")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")

def test_airport_codes():
    """Test airport code extraction"""
    print("\n🔍 Testing airport code extraction...")
    
    airport_test_cases = [
        "Goa trip",
        "Delhi to Mumbai",
        "Bangalore vacation",
        "Chennai weekend",
        "Kolkata to Hyderabad"
    ]
    
    for i, text in enumerate(airport_test_cases, 1):
        print(f"\n✈️  Airport Test {i}: {text}")
        
        try:
            payload = {"text": text}
            response = requests.post(
                f"{BASE_URL}/api/trip/plan",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                flight = data['trip_data']['flight']
                print(f"   From: {flight['from']} → To: {flight['to']}")
            elif response.status_code == 400:
                data = response.json()
                if data.get('status') == 'insufficient_data':
                    print(f"   ⚠️  Insufficient data - Missing: {data['missing_fields']}")
                else:
                    print(f"   ❌ Error: {data.get('message', 'Unknown')}")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Cannot connect to API")
            break
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        time.sleep(0.5)

def test_fill_missing_fields():
    """Test filling in missing fields from previous response"""
    print("\n🔍 Testing fill missing fields functionality...")
    
    # First request - should return missing fields
    print("📝 Step 1: Initial request with missing source and date")
    initial_text = "I want to visit Goa for 3 days"
    
    try:
        payload = {"text": initial_text}
        response = requests.post(
            f"{BASE_URL}/api/trip/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Initial request returned missing fields as expected")
            print(f"Missing fields: {data['missing_fields']}")
            
            # Now use the response to fill missing fields
            print("\n📝 Step 2: Filling missing source")
            fill_source_text = "From Delhi"
            fill_source_payload = {
                "text": fill_source_text,
                "trip_data": data['trip_data']
            }
            
            response2 = requests.post(
                f"{BASE_URL}/api/trip/plan",
                json=fill_source_payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response2.status_code == 400:
                data2 = response2.json()
                print("✅ Source filled, still missing date")
                print(f"Updated missing fields: {data2['missing_fields']}")
                print(f"Flight from now: {data2['trip_data']['flight']['from']}")
                
                # Now fill the date
                print("\n📝 Step 3: Filling missing date")
                fill_date_text = "tomorrow"
                fill_date_payload = {
                    "text": fill_date_text,
                    "trip_data": data2['trip_data']
                }
                
                response3 = requests.post(
                    f"{BASE_URL}/api/trip/plan",
                    json=fill_date_payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response3.status_code == 200:
                    final_data = response3.json()
                    print("✅ All fields filled successfully!")
                    print(f"Final flight: {final_data['flight']['from']} → {final_data['flight']['to']}")
                    print(f"Departure date: {final_data['flight']['depart_date']}")
                    print(f"Adults: {final_data['flight']['adults']}")
                else:
                    print(f"❌ Failed to fill date: {response3.status_code}")
                    print(f"Response: {response3.text}")
            else:
                print(f"❌ Unexpected response when filling source: {response2.status_code}")
                
        else:
            print(f"❌ Expected 400, got {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_fill_missing_fields_advanced():
    """Test more complex scenarios for filling missing fields"""
    print("\n🔍 Testing advanced fill missing fields scenarios...")
    
    # Test filling multiple fields at once
    print("📝 Test: Fill source and date in one request")
    
    # Initial incomplete request
    initial_payload = {
        "text": "Goa vacation for 2 adults"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/trip/plan",
            json=initial_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Initial request returned missing fields")
            print(f"Missing: {data['missing_fields']}")
            
            # Fill multiple fields at once
            fill_all_payload = {
                "text": "From Delhi to Goa tomorrow",
                "trip_data": data['trip_data']
            }
            
            response2 = requests.post(
                f"{BASE_URL}/api/trip/plan",
                json=fill_all_payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response2.status_code == 200:
                final_data = response2.json()
                print("✅ All fields filled successfully in one request!")
                print(f"Flight: {final_data['flight']['from']} → {final_data['flight']['to']}")
                print(f"Date: {final_data['flight']['depart_date']}")
                print(f"Adults: {final_data['flight']['adults']}")
            else:
                print(f"❌ Failed to fill all fields: {response2.status_code}")
                print(f"Response: {response2.text}")
        else:
            print(f"❌ Expected 400, got {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_specific_scenario():
    """Test the specific scenario mentioned by user"""
    print("\n🔍 Testing specific scenario: 'From Delhi'")
    
    # Test the exact case mentioned by user
    print("📝 Test: Fill source with 'From Delhi'")
    
    payload = {
        "text": "From Delhi",
        "trip_data": {
            "flight": {
                "from": "",
                "to": "GOI",
                "depart_date": "",
                "adults": 2,
                "intl": "n"
            },
            "hotel": {
                "cityId": "1138",
                "city": "Goa",
                "state": "Goa",
                "country": "IN",
                "checkInDate": "",
                "checkOutDate": "",
                "version": "V2"
            }
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/trip/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"Missing fields: {data['missing_fields']}")
            if 'source' not in data['missing_fields']:
                print("✅ Source field was successfully filled!")
                print(f"Flight from: {data['trip_data']['flight']['from']}")
            else:
                print("❌ Source field is still missing")
        elif response.status_code == 200:
            data = response.json()
            print("✅ All fields filled successfully!")
            print(f"Flight: {data['flight']['from']} → {data['flight']['to']}")
            print(f"Date: {data['flight']['depart_date']}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_text_extraction():
    """Test the text extraction functions directly"""
    print("\n🔍 Testing text extraction functions...")
    
    test_texts = [
        "From Delhi",
        "From Mumbai to Goa",
        "Delhi to Bangalore",
        "Goa trip",
        "From Delhi tomorrow"
    ]
    
    for text in test_texts:
        print(f"\n📝 Testing: '{text}'")
        
        try:
            # Test the extraction functions
            from controllers.trip_controller import extract_source_and_destination, extract_adults_count, extract_dates
            
            source_city, dest_city = extract_source_and_destination(text)
            adults_count = extract_adults_count(text)
            dates = extract_dates(text)
            
            print(f"   Source: {source_city['city'] if source_city else 'None'}")
            print(f"   Destination: {dest_city['city'] if dest_city else 'None'}")
            print(f"   Adults: {adults_count}")
            print(f"   Dates: {dates}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        time.sleep(0.5)

def test_specific_date_formats():
    """Test specific date formats that should work"""
    print("\n🔍 Testing specific date formats...")
    
    date_test_cases = [
        "From Delhi for 21st September 2025",
        "From Mumbai to Goa on 25th December",
        "From Bangalore to Chennai on 15th March 2025",
        "From Kolkata to Jaipur on 30th April"
    ]
    
    for i, text in enumerate(date_test_cases, 1):
        print(f"\n📅 Date Format Test {i}: {text}")
        
        try:
            payload = {"text": text}
            response = requests.post(
                f"{BASE_URL}/api/trip/plan",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                trip_data = response.json()
                print(f"   ✅ Success - Date recognized!")
                print(f"   Flight: {trip_data['flight']['from']} → {trip_data['flight']['to']}")
                print(f"   Departure date: {trip_data['flight']['depart_date']}")
                print(f"   Check-in: {trip_data['hotel']['checkInDate']}")
                print(f"   Check-out: {trip_data['hotel']['checkOutDate']}")
            elif response.status_code == 400:
                data = response.json()
                if 'missing_fields' in data:
                    print(f"   ⚠️  Still missing fields: {data['missing_fields']}")
                    if 'departure_date' not in data['missing_fields']:
                        print("   ✅ Date field was recognized!")
                    else:
                        print("   ❌ Date field still not recognized")
                else:
                    print(f"   ❌ Unexpected error response: {data}")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Cannot connect to API")
            break
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        time.sleep(0.5)

def test_september_date_specific():
    """Test the specific September date format mentioned by user"""
    print("\n🔍 Testing September date format specifically...")
    
    # Test the exact case mentioned by user
    print("📝 Test: 'From Delhi for 21st September 2025'")
    
    payload = {
        "text": "From Delhi for 21st September 2025",
        "trip_data": {
            "flight": {
                "from": "",
                "to": "GOI",
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
                "cityId": "1138",
                "city": "Goa",
                "state": "Goa",
                "country": "IN",
                "checkInDate": "",
                "checkOutDate": "",
                "version": "V2"
            }
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/trip/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! All fields filled")
            print(f"Flight: {data['flight']['from']} → {data['flight']['to']}")
            print(f"Departure date: {data['flight']['depart_date']}")
            print(f"Check-in: {data['hotel']['checkInDate']}")
            print(f"Check-out: {data['hotel']['checkOutDate']}")
            
            # Verify the date is actually September, not August
            if "09" in data['flight']['depart_date'] or "21/09" in data['flight']['depart_date']:
                print("✅ Date correctly parsed as September!")
            else:
                print("❌ Date still not parsed correctly")
                
        elif response.status_code == 400:
            data = response.json()
            if 'missing_fields' in data:
                print(f"⚠️  Still missing fields: {data['missing_fields']}")
                if 'departure_date' not in data['missing_fields']:
                    print("✅ Date field was recognized!")
                else:
                    print("❌ Date field still not recognized")
            else:
                print(f"❌ Unexpected error response: {data}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_2026_year_specific():
    """Test the specific 2026 year format mentioned by user"""
    print("\n🔍 Testing 2026 year format specifically...")
    
    # Test the exact case mentioned by user
    print("📝 Test: 'From Delhi for 21st September 2026'")
    
    payload = {
        "text": "From Delhi for 21st September 2026",
        "trip_data": {
            "flight": {
                "from": "",
                "to": "GOI",
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
                "cityId": "1138",
                "city": "Goa",
                "state": "Goa",
                "country": "IN",
                "checkInDate": "",
                "checkOutDate": "",
                "version": "V2"
            }
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/trip/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! All fields filled")
            print(f"Flight: {data['flight']['from']} → {data['flight']['to']}")
            print(f"Departure date: {data['flight']['depart_date']}")
            print(f"Check-in: {data['hotel']['checkInDate']}")
            print(f"Check-out: {data['hotel']['checkOutDate']}")
            
            # Verify the year is actually 2026, not 2025
            if "2026" in data['flight']['depart_date']:
                print("✅ Year correctly parsed as 2026!")
            else:
                print(f"❌ Year incorrectly parsed as: {data['flight']['depart_date']}")
                print("   Expected: 21/09/2026")
                
        elif response.status_code == 400:
            data = response.json()
            if 'missing_fields' in data:
                print(f"⚠️  Still missing fields: {data['missing_fields']}")
                if 'departure_date' not in data['missing_fields']:
                    print("✅ Date field was recognized!")
                else:
                    print("❌ Date field still not recognized")
            else:
                print(f"❌ Unexpected error response: {data}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main test function"""
    print("🚀 TripVoice API Test Suite - Fill Missing Fields")
    print("=" * 60)
    
    # Test health endpoint
    test_health_endpoint()
    
    # Test cities endpoint
    test_cities_endpoint()
    
    # Test trip planning
    test_trip_planning()
    
    # Test missing source scenarios
    test_missing_source_scenarios()
    
    # Test date extraction
    test_date_extraction()
    
    # Test airport codes
    test_airport_codes()
    
    # Test error cases
    test_error_cases()
    
    # Test fill missing fields
    test_fill_missing_fields()
    test_fill_missing_fields_advanced()
    
    # Test specific scenario
    test_specific_scenario()
    
    # Test text extraction functions
    test_text_extraction()
    
    # Test specific date formats
    test_specific_date_formats()
    
    # Test September date specific format
    test_september_date_specific()
    
    # Test 2026 year specific format
    test_2026_year_specific()
    
    print("\n" + "=" * 60)
    print("🏁 Test suite completed!")
    print("\n💡 To test with Postman:")
    print("1. POST to http://localhost:5000/api/trip/plan")
    print("2. Set Content-Type: application/json")
    print("3. Body: {\"text\": \"From Delhi to Goa for 2 adults\"}")
    print("\n🌍 Test cities endpoint:")
    print("GET http://localhost:5000/api/trip/cities")
    print("\n⚠️  New Features:")
    print("- Airport codes (DEL, BOM, BLR, MAA, GOI, etc.)")
    print("- Source/destination extraction (BOTH required)")
    print("- Date extraction (only when explicitly mentioned)")
    print("- Clean response format (no extra fields)")
    print("- Fill missing fields from previous responses")
    print("- Auto-calculated check-in/check-out dates from departure date")
    print("- Advanced date format recognition (21st September 2025, etc.)")
    print("- Actual date parsing (not just default dates)")
    print("- Proper year parsing (2026, 2025, etc.)")
    print("- Missing field detection with user-friendly names")
    print("\n🔍 Response Format:")
    print("✅ Success (200): Returns trip_data directly")
    print("❌ Error (400): Returns {missing_fields: [...], trip_data: {...}}")
    print("❌ Server Error (500): Returns {missing_fields: ['server_error'], trip_data: null}")
    print("\n🔄 Fill Missing Fields:")
    print("Send: {\"text\": \"From Delhi\", \"trip_data\": {...previous_response...}}")
    print("API will update missing fields based on new text input")
    print("\n📅 Date Logic:")
    print("- Only departure_date is required from user")
    print("- Check-in and check-out dates are auto-calculated")
    print("- Supports formats: '21st September 2026', '25th December 2025', 'tomorrow', etc.")
    print("- Actually parses the specified date (not default dates)")
    print("- Correctly handles years (2026, 2025, etc.)")
    print("\n🐛 Debug Info:")
    print("Check console output for DEBUG messages when filling missing fields")

if __name__ == "__main__":
    main() 