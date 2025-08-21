#!/usr/bin/env python3
"""
Script to create sample image files for the TripVoice service
"""

import os

def create_sample_images():
    """Create sample image files"""
    
    # Create directories if they don't exist
    directories = [
        'images/flights',
        'images/hotels', 
        'images/airlines',
        'images/amenities',
        'images/packages'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Flight images
    flight_images = [
        'aircraft_boeing.jpg',
        'aircraft_airbus.jpg',
        'aircraft_boeing_787.jpg'
    ]
    
    # Hotel images
    hotel_images = []
    room_images = []
    for i in range(1, 51):  # Create 50 hotel images
        hotel_images.append(f'hotel_{i:03d}.jpg')
        room_images.append(f'room_{i:03d}.jpg')
    
    # Airline logos
    airline_images = [
        'indigo.png',
        'vistara.png', 
        'air_india.png',
        'spicejet.png',
        'goair.png',
        'airasia_india.png'
    ]
    
    # Amenity images
    amenity_images = [
        'wifi.jpg',
        'pool.jpg',
        'gym.jpg',
        'spa.jpg',
        'restaurant.jpg',
        'bar.jpg',
        'room_service.jpg',
        'business_center.jpg',
        'concierge.jpg',
        'parking.jpg'
    ]
    
    # Package images
    package_images = [
        'luxury_package.jpg',
        'budget_package.jpg',
        'comfort_package.jpg',
        'adventure_package.jpg',
        'romantic_package.jpg'
    ]
    
    # Create all image files
    all_images = {
        'images/flights': flight_images,
        'images/hotels': hotel_images + room_images,
        'images/airlines': airline_images,
        'images/amenities': amenity_images,
        'images/packages': package_images
    }
    
    for directory, images in all_images.items():
        for image in images:
            filepath = os.path.join(directory, image)
            if not os.path.exists(filepath):
                # Create a simple text file as placeholder
                with open(filepath, 'w') as f:
                    f.write(f"Sample image: {image}\n")
                    f.write("This is a placeholder image file.\n")
                    f.write("In a real application, this would be an actual image file.\n")
                print(f"Created: {filepath}")
    
    print(f"\nCreated {sum(len(images) for images in all_images.values())} sample image files")
    print("Image directories:")
    for directory in directories:
        count = len(os.listdir(directory))
        print(f"  {directory}: {count} files")

if __name__ == "__main__":
    create_sample_images()
