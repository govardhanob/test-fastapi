# Deployment

This API runs locally with Uvicorn and deploys to Firebase Hosting through Cloud Run.

## Local

Keep your Firebase service account JSON local. It is ignored by Git and Docker.

```bash
cp .env.example .env
uvicorn app.main:app --reload
```

The app checks credentials in this order:

1. `FIREBASE_SERVICE_ACCOUNT`
2. `GOOGLE_APPLICATION_CREDENTIALS`
3. `firebase-service-account.json`
4. `app/test-5f434-firebase-adminsdk-fbsvc-911d3ec5b0.json`
5. Cloud Run / Google default credentials

## Cloud Run

```bash
gcloud auth login
gcloud config set project hisbee
gcloud auth list
```

Make sure the active `gcloud` account owns or can deploy to `hisbee`.
It needs permission to enable APIs, deploy Cloud Run services, and update Cloud Run IAM.

```bash
gcloud run deploy fastapi-firebase-api \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --project hisbee
```

If `/docs` returns `403 Forbidden`, make the Cloud Run service public:

```bash
gcloud run services add-iam-policy-binding fastapi-firebase-api \
  --region asia-south1 \
  --project hisbee \
  --member allUsers \
  --role roles/run.invoker
```

If Firestore permissions fail, grant the Cloud Run runtime service account Firestore access:

```bash
PROJECT_ID=hisbee
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/datastore.user"
```

## Firebase Hosting

`firebase.json` rewrites all Hosting requests to the Cloud Run service.

```bash
firebase login
firebase deploy --only hosting --project hisbee
```

After deploy:

```text
https://hisbee.web.app/docs
https://hisbee.web.app/health
```
