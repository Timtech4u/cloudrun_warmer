# Cloud Run Warmer
> A warmer service that periodically makes requests to Cloud Run services.

Cloud Run services often requires downloading the container image and starting the container before it is accessible. This is called a **cold start** and it occurs due to Cloud Run's scale to zero ability.

This tool prevents cold start by making scheduled requests that warms up Cloud Run services. 


## How to use
- [Generate Service Account JSON Key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and update [code](auth.py#L72) OR generate and set access token `ACCESS_TOKEN` [here](main.py#L9) and `PROJECT_ID` [here](main.py#L13) env vars.

`gcloud auth application-default print-access-token`

- Deploy this repo to Cloud Functions

`gcloud functions deploy cloudrun_warmer --runtime python37 --trigger-http`

- Set up Cloud Scheduler Job
``` 
gcloud scheduler jobs create http cloudrun_warmer_job --schedule "0 * * * *" --uri "https://us-central1-myproject.cloudfunctions.net/cloudrun_warmer" --http-method GET
```

## How it works
- Attempts to retrieve access token and project ID
- Fetches the list of all Cloud Run services on project
- Make requests to each service with a timeout of 5 secs


## Tools
- [Cloud Function](https://cloud.google.com/functions)
- [Cloud Scheduler](https://cloud.google.com/scheduler)
- [Cloud Run API](https://cloud.google.com/run/docs/reference/rest/)
- [Python Requests](https://github.com/psf/requests)
- [GCP Access Token Auth](https://gist.github.com/Timtech4u/f38d53671ccbaf802820b2e1f0e3f6c8)
