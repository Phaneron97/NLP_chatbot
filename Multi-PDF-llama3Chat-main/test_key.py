import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GROQ_API_KEY")

# Check if the API key is loaded correctly
if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

print(f"Using API Key: {api_key[:4]}****")  # Partial print for security

# API URL
url = "https://api.groq.com/openai/v1/models"

# Headers for the request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Print the response for debugging
print(f"Response Status Code: {response.status_code}")
print(response.json())
