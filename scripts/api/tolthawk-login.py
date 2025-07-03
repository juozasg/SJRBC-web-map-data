#!/usr/bin/env python3
"""
Script to get API token from Tolthawk API.
Reads email and password from 'tolthawk-login' file and saves token to 'tolthawk-token' file.
"""

import requests
import json
import sys
import os

def read_credentials():
    """Read email and password from tolthawk-login file."""
    try:
        with open('tolthawk-login', 'r') as f:
            lines = f.read().strip().split('\n')
            if len(lines) >= 2:
                email = lines[0].strip()
                password = lines[1].strip()
                return email, password
            else:
                raise ValueError("Login file must contain at least 2 lines (email and password)")
    except FileNotFoundError:
        print("Error: tolthawk-login file not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading credentials: {e}")
        sys.exit(1)

def get_api_token(email, password, expires=30):
    """Get API token from Tolthawk API."""
    url = "https://sensors.tolthawk.com/api/token"
    payload = {
        "Email": email,
        "Password": password,
        "Expires": expires
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Assuming the API returns the token in JSON format
        token_data = response.json()
        
        # Extract token (adjust this based on actual API response format)
        if 'token' in token_data:
            return token_data['token']
        elif 'access_token' in token_data:
            return token_data['access_token']
        else:
            # If token is in a different field or the response is just the token string
            return token_data
            
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response text: {response.text}")
        sys.exit(1)

def save_token(token):
    """Save token to tolthawk-token file."""
    try:
        with open('tolthawk-token', 'w') as f:
            f.write(str(token))
        print("Token successfully saved to tolthawk-token file")
    except Exception as e:
        print(f"Error saving token: {e}")
        sys.exit(1)

def tolthawk_login():
    """Main function."""
    print("Reading credentials...")
    email, password = read_credentials()
    print(f"Using email: {email}")
    
    print("Requesting API token...")
    token = get_api_token(email, password)
    
    print("Saving token...")
    save_token(token)
    
    print("Done!")

if __name__ == "__main__":
    tolthawk_login()