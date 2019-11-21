import os
import requests
from auth.auth import getAccessToken

# Get access token from enviroment variable OR
# Use getAccessToken() method to retrieve access token
access_token = os.environ.get("ACCESS_TOKEN", getAccessToken())

# Get project ID from enviroment variable
project_id = os.environ.get("PROJECT_ID")

# Get region from enviroment variable
region = os.environ.get("REGION", "us-central1")

# Filters to help skip services by images or names
# Get GCR Images to Skip from enviroment variable
disallowed_images = os.environ.get("DISALLOWED_IMAGES", [])

# Get Services Name to Skip from enviroment variable
disallowed_services = os.environ.get("DISALLOWED_SERVICES", [])

# Request header using access token
auth_header = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}


def cloudrun_warmer(request):
    try:
        services = requests.get(
            f"https://run.googleapis.com/v1alpha1/projects/{project_id}/locations/{region}/services",
            headers=auth_header).json()

        if 'items' in services:
            for service in services['items']:
                if service['metadata']['name'] not in disallowed_services and service['metadata']['annotations']['client.knative.dev/user-image'] not in disallowed_images:
                    try:
                        # Make request to Cloud Run service domain with a timeout of 5secs
                        status = requests.get(
                            service['status']['domain'], timeout=5).status_code
                        print(
                            f"Service Name: {service['metadata']['name']} | Status Code: {status}")
                    except Exception as e:
                        print(f"An Error Occurred: {e}")

        return f"Total services warmed up: {len(services['items'])}"
    except Exception as e:
        return f"An Error Occurred while fetching services: {e}"