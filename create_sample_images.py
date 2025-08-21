#!/usr/bin/env python3
"""
Script to create sample images for the TripVoice project
"""

import os

def create_placeholder_file(filepath, content):
    """Create a placeholder file with content"""
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created: {filepath}")

def create_sample_images():
    """Create all sample images for the project"""
    
    # Create images directory structure
    categories = ['packages', 'flights', 'hotels', 'amenities', 'airlines']
    
    for category in categories:
        os.makedirs(f'images/{category}', exist_ok=True)
    
    # Package images
    package_images = [
        ('budget_package.jpg', 'Budget Explorer Package - Sample Image'),
        ('midrange_package.jpg', 'Mid-Range Comfort Package - Sample Image'),
        ('luxury_package.jpg', 'Luxury Premium Package - Sample Image'),
        ('adventure_package.jpg', 'Adventure Package - Sample Image'),
        ('family_package.jpg', 'Family Package - Sample Image')
    ]
    
    for filename, content in package_images:
        create_placeholder_file(f'images/packages/{filename}', content)
    
    # Flight images
    flight_images = [
        ('aircraft_boeing.jpg', 'Boeing Aircraft - Sample Image'),
        ('aircraft_airbus.jpg', 'Airbus Aircraft - Sample Image'),
        ('flight_cockpit.jpg', 'Flight Cockpit - Sample Image'),
        ('flight_takeoff.jpg', 'Flight Takeoff - Sample Image')
    ]
    
    for filename, content in flight_images:
        create_placeholder_file(f'images/flights/{filename}', content)
    
    # Hotel images
    hotel_images = [
        ('hotel_exterior.jpg', 'Hotel Exterior - Sample Image'),
        ('hotel_lobby.jpg', 'Hotel Lobby - Sample Image'),
        ('hotel_room.jpg', 'Hotel Room - Sample Image'),
        ('hotel_pool.jpg', 'Hotel Pool - Sample Image'),
        ('hotel_spa.jpg', 'Hotel Spa - Sample Image'),
        ('hotel_restaurant.jpg', 'Hotel Restaurant - Sample Image')
    ]
    
    for filename, content in hotel_images:
        create_placeholder_file(f'images/hotels/{filename}', content)
    
    # Amenity images
    amenity_images = [
        ('wifi.jpg', 'WiFi - Sample Image'),
        ('pool.jpg', 'Swimming Pool - Sample Image'),
        ('spa.jpg', 'Spa & Wellness - Sample Image'),
        ('restaurant.jpg', 'Restaurant - Sample Image'),
        ('gym.jpg', 'Fitness Center - Sample Image'),
        ('concierge.jpg', 'Concierge - Sample Image'),
        ('parking.jpg', 'Parking - Sample Image'),
        ('business_center.jpg', 'Business Center - Sample Image')
    ]
    
    for filename, content in amenity_images:
        create_placeholder_file(f'images/amenities/{filename}', content)
    
    # Airline logos
    airline_logos = [
        ('indigo.png', 'IndiGo Logo - Sample Image'),
        ('airindia.png', 'Air India Logo - Sample Image'),
        ('vistara.png', 'Vistara Logo - Sample Image'),
        ('spicejet.png', 'SpiceJet Logo - Sample Image'),
        ('airasia.png', 'AirAsia Logo - Sample Image'),
        ('akasa.png', 'Akasa Air Logo - Sample Image')
    ]
    
    for filename, content in airline_logos:
        create_placeholder_file(f'images/airlines/{filename}', content)
    
    print("\n✅ All sample images created successfully!")
    print("📁 Images are stored in the 'images/' directory")
    print("🌐 Access them via: http://localhost:5000/images/<category>/<filename>")
    print("\n📝 Note: These are placeholder files. Replace with actual images for production use.")

if __name__ == "__main__":
    create_sample_images()
