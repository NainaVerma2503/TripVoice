#!/usr/bin/env python3

import os
import ssl
from openai import AzureOpenAI
import json

# Test Azure OpenAI API directly
try:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY", ""),
        api_version=os.getenv("AZURE_API_VERSION", ""),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "")
    )
    
    print("Testing OpenAI API...")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a travel planning assistant."},
            {"role": "user", "content": "Extract city from: From Delhi for 21st September 2026"}
        ],
        max_tokens=100,
        temperature=0.1
    )
    
    print("Success! Response:")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    
    # Try to get more details about the error
    if hasattr(e, 'response'):
        print(f"Response status: {e.response.status_code}")
        print(f"Response text: {e.response.text}") 