import requests
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get backend and sentiment analyzer URLs with fallbacks
backend_url = os.getenv("backend_url", "http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", "http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """Send a GET request to the backend API with optional query parameters."""
    try:
        # Encode query parameters safely
        params = urllib.parse.urlencode(kwargs) if kwargs else ""
        request_url = f"{backend_url}{endpoint}?{params}"

        print(f"GET from {request_url}")

        # Perform the GET request
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for HTTP 4xx/5xx responses

        return response.json()

    except requests.exceptions.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None


def analyze_review_sentiments(text):
    """Analyze sentiment of a given text using the sentiment analyzer API."""
    try:
        request_url = f"{sentiment_analyzer_url}analyze/"
        request_url += urllib.parse.quote(text)
        response = requests.get(request_url)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as err:
        print(f"Unexpected error occurred: {err}")
        return None


def post_review(data_dict):
    """Submit a review to the backend API."""
    try:
        request_url = f"{backend_url}/insert_review"
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()

        print(response.json())
        return response.json()

    except requests.exceptions.RequestException as err:
        print(f"Network exception occurred: {err}")
        return None
