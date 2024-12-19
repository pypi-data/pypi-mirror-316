from . import gcp
from googleapiclient.discovery import build
from google.cloud import storage, aiplatform 


# Access Vertex AI
def get_session():
    credentials = gcp.get_credentials()
    aiplatform.init(project=credentials.project_id, credentials=credentials)
