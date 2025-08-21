#!/usr/bin/env python3
"""
Environment Setup Script for TripVoice API
This script helps you create a .env file with your Azure OpenAI credentials
"""

import os

def create_env_file():
    """Create .env file with user input"""
    
    print("🚀 TripVoice API Environment Setup")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📝 Please provide your Azure OpenAI credentials:")
    
    # Get user input
    endpoint = input("Azure OpenAI Endpoint (required): ").strip()
    if not endpoint:
        print("❌ Endpoint is required!")
        return
    
    api_key = input("Azure OpenAI API Key (required): ").strip()
    if not api_key:
        print("❌ API Key is required!")
        return
    
    deployment = input("Deployment Name (required): ").strip()
    if not deployment:
        print("❌ Deployment name is required!")
        return
    
    api_version = input("API Version (required): ").strip()
    if not api_version:
        print("❌ API version is required!")
        return
    
    port = input("Flask Port (press Enter for default): ").strip()
    if not port:
        port = "5001"
    
    # Create .env content
    env_content = f"""# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT={endpoint}
AZURE_OPENAI_KEY={api_key}
AZURE_OPENAI_DEPLOYMENT={deployment}
AZURE_API_VERSION={api_version}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT={port}
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print(f"📁 Location: {os.path.abspath('.env')}")
        print("\n🔒 Security Note: .env is already in .gitignore")
        print("🚀 You can now run: python3 app.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file() 