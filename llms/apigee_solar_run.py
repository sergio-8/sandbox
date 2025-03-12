curl -L https://raw.githubusercontent.com/apigee/apigeecli/main/downloadLatest.sh | sh -

export PATH=$PATH:$HOME/.apigeecli/bin


git clone https://github.com/tyayers/apigee-genai-solar-demo.git

cd apigee-genai-solar-demo


#Get a Google Maps API key

cp 1_env.sh 1_env.dev.sh

export PROJECT=YOUR GCP PROJECT ID
export REGION=YOUR GCP REGION
export APIGEE_ENVIRONMENT=YOUR ENVIRONMENT


#activate venv
source 1_env.dev.sh

gcloud config set project $PROJECT

gcloud services enable aiplatform.googleapis.com
gcloud services enable solar.googleapis.com
gcloud services enable geocoding-backend.googleapis.com

#create service account

gcloud iam service-accounts create solarservice \
    --description="Solar service account" \
    --display-name="Solar service"


gcloud projects add-iam-policy-binding $PROJECT \
--member="serviceAccount:solarservice@$PROJECT.iam.gserviceaccount.com" \
--role="roles/aiplatform.user"


apigeecli kvms create -e $APIGEE_ENVIRONMENT -n solar-keys -o $PROJECT -t $(gcloud auth print-access-token)


{
        "name": "solar-keys",
        "encrypted": true
}

GMAPS_KEY=YOUR_GMAPS_KEY

apigeecli kvms entries create -m solar-keys -k gmaps_key -l $GMAPS_KEY -e $APIGEE_ENVIRONMENT -o $PROJECT -t $(gcloud auth print-access-token)


cd api-proxies/Solar-Service-v1

zip Solar-Service-v1.zip -r .

apigeecli apis import -o $PROJECT -f . -t $(gcloud auth print-access-token)



apigeecli apis deploy -n Solar-Service-v1 -o $PROJECT -e $APIGEE_ENVIRONMENT -t $(gcloud auth print-access-token) -s solarservice@$PROJECT.iam.gserviceaccount.com --ovr



curl -X POST "$URL" -i \
-H "Content-Type: application/json" \
--data @- << EOF

{
  "address": "Tucholskystr 2, 10117 Berlin"
}
EOF


PRODUCT_NAME="Solar-API-v1"
apigeecli products create -n "$PRODUCT_NAME" \
  -m "$PRODUCT_NAME" \
  -o "$PROJECT" -e $APIGEE_ENVIRONMENT \
  -f auto -p "Solar-Service-v1" -t $(gcloud auth print-access-token)

DEVELOPER_EMAIL="example-developer@cymbalgroup.com"


apigeecli developers create -n "$DEVELOPER_EMAIL" \
  -f "Example" -s "Developer" \
  -u "$DEVELOPER_EMAIL" -o "$PROJECT" -t $(gcloud auth print-access-token)



APP_NAME=example-app-1
apigeecli apps create --name "$APP_NAME" \
  --email "$DEVELOPER_EMAIL" \
  --prods "$PRODUCT_NAME" \
  --org "$PROJECT" --token $(gcloud auth print-access-token)


API_KEY="replace with consumerKey field from last command"


curl -X POST "$URL" -i \
-H "Content-Type: application/json" \
-H "x-api-key: $API_KEY" \
--data @- << EOF

{
  "address": "Tucholskystr 2, 10117 Berlin"
}
EOF



