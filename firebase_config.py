from decouple import config

firebase_config = {
    "apiKey": config('API_KEY'),
    "authDomain": config('AUTH_DOMAIN'),
    "databaseURL": config('DATABASE_URL'),
    "projectId": config('PROJECT_ID'),
    "storageBucket": config('STORAGE_BUCKET'),
    "messagingSenderId": config('MESSAGE_SENDER_ID'),
    "appId": config('APP_ID'),
    "measurementId": config('MEASURE_ID')
  }

