import os
from google.cloud import firestore

# Ajusta la ruta si no está en la raíz
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

db = firestore.Client()
