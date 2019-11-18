import os
import requests
from auth import getAccessToken
from filters import disallowed_images, disallowed_services

# Get access token from enviroment variable OR
# Use getAccessToken() method to retrieve access token
access_token = os.environ.get("ACCESS_TOKEN", getAccessToken())

# Get project ID from enviroment variable
project_id = os.environ.get("PROJECT_ID")

# Change this if your Cloud Run services are in a different location
region = "us-central1"

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
                if 'client.knative.dev/user-image' in service['metadata']['annotations'] 
                    and service['metadata']['name'] not in disallowed_services
                    and service['metadata']['annotations']['client.knative.dev/user-image'] not in disallowed_images:
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
