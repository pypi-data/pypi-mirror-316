from . import gcp
from googleapiclient.discovery import build
from google.cloud import storage, aiplatform 

# Access Cloud Storage

def get_session():
    storage_client = storage.Client(credentials=gcp.get_credentials())
    return storage_client
