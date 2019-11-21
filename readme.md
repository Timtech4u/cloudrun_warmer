# Cloud Run Warmer
> A warmer service that periodically makes requests to Cloud Run services.

Cloud Run services often requires downloading the container image and starting the container before it is accessible. This is called a **cold start** and it occurs due to Cloud Run's scale to zero ability.

This tool prevents cold start by making scheduled requests that warms up Cloud Run services.
You can read more about how to minimize Cloud Run Cold Starts John's article [here](https://www.jhanley.com/google-cloud-run-minimizing-cold-starts/)

Note that this tool best fits when you have multiple Cloud Run services on a project and you do not want to setup individual Cloud Scheduler Jobs to warm each service.

## How to use
- [Generate Service Account JSON Key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and update [code](auth.py#L72) OR generate and set access token `ACCESS_TOKEN` [here](main.py#L8) and `PROJECT_ID` [here](main.py#L11) env vars.

`gcloud auth application-default print-access-token`

- Deploy this repo to Cloud Functions

`gcloud functions deploy cloudrun_warmer --runtime python37 --trigger-http`

- Set up Cloud Scheduler Job with Function's URL
``` 
gcloud scheduler jobs create http cloudrun_warmer_job --schedule "0 * * * *" --uri "https://us-central1-myproject.cloudfunctions.net/cloudrun_warmer" --http-method GET
```

## How it works
- Attempts to retrieve access token and project ID
- Fetches the list of all Cloud Run services on project
- Make requests to each service with a timeout of 5 secs

## Setting filters
- To prevent the warmer from making requests to certain service(s), you can add the service image or name to this [file](filters.py) for example:
```
disallowed_services = ['myservice']
disallowed_images = ['gcr.io/myproject/myimage:latest']
```

## Tools Used
- [Cloud Function](https://cloud.google.com/functions)
- [Cloud Scheduler](https://cloud.google.com/scheduler)
- [Cloud Run API](https://cloud.google.com/run/docs/reference/rest/)
- [Python Requests](https://github.com/psf/requests)
- [GCP Access Token Auth](https://gist.github.com/Timtech4u/f38d53671ccbaf802820b2e1f0e3f6c8)

> If you want to complete this steps using a GUI or Cloud Console, check out my article on [Scheduling periodic jobs with Cloud Scheduler ⏰](https://fullstackgcp.com/scheduling-periodic-jobs-with-cloud-scheduler-alarm-clock-ck35lo6g3002eb6s13btat0n3)
