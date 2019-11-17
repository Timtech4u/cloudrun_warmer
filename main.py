import os
import requests
from auth import getAccessToken


# Get access token from enviroment variable OR
# Use getAccessToken() method to retrieve access token
# access_token = os.environ.get("ACCESS_TOKEN", getAccessToken())
access_token = "ya29.Iq8BsQf8SF-thmm2gICWL3R8MvvOL7T71WNsde7eNmp6uv2LaWuPmFEpay62AySEf9CERQha9rwDgUpmVrmziwEuSofyXirGOZ0Y7wGGvZ9pE95frtzagOG_ea4UmfGpb0TGl7C5StCsnvQxzANch7tMNRYSB8TcUsQEDqhxCQH15r3zEnPDok-dErYyue6R6WCpA3jeyaC4Sf2EeN6WbOsFuIpLXSWcCTc5F7nbcfmaQw"

# Get project ID from enviroment variable
# project_id = os.environ.get("PROJECT_ID")
project_id = "mercuriemart"

# Request header using access token
auth_header = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}


def cloudrun_warmer(request):
    try:
        services = requests.get(
            f"https://run.googleapis.com/v1alpha1/projects/{project_id}/locations/us-central1/services", headers=auth_header).json()

        if 'items' in services:
            for service in services['items']:
                if 'client.knative.dev/user-image' in service['metadata']['annotations']:
                    try:
                        # Make request Cloud Run service with a timeout of 5secs
                        status = requests.get(
                            service['status']['domain'], timeout=5).status_code
                        print(
                            f"Service Name: {service['metadata']['name']} | Status Code: {status}")
                    except Exception as e:
                        print(f"An Error Occurred: {e}")

        return f"Total services warmed up: {len(services['items'])}"
    except Exception as e:
        return f"An Error Occurred while fetching services: {e}"

print(cloudrun_warmer(1))