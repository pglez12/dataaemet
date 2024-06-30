docker build -t gcr.io/aemet-data/aemet-img .
docker push gcr.io/aemet-data/aemet-img
gcloud run deploy data-load --image gcr.io/aemet-data/aemet-img --platform managed --region europe-west1 --allow-unauthenticated --port 8000