# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from google.cloud import documentai_v1 as documentai
from google.cloud import firestore

# --- Environment Variables ---
# These will be set in the Cloud Function's configuration
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_LOCATION = os.environ.get("GCP_LOCATION")
DOCAI_PROCESSOR_ID = os.environ.get("DOCAI_PROCESSOR_ID")
FIRESTORE_COLLECTION = os.environ.get("FIRESTORE_COLLECTION")

def process_document_from_gcs(event, context):
    """
    Cloud Function triggered by a GCS event to process a document with Document AI
    and save the result to Firestore.
    """
    bucket_name = event["bucket"]
    file_name = event["name"]
    gcs_uri = f"gs://{bucket_name}/{file_name}"
    
    print(f"--- Processing file: {gcs_uri} ---")

    try:
        # Initialize clients
        docai_client = documentai.DocumentProcessorServiceClient(
            client_options={"api_endpoint": f"{GCP_LOCATION}-documentai.googleapis.com"}
        )
        firestore_client = firestore.Client()

        # Configure and send the DocAI request
        processor_name = docai_client.processor_path(GCP_PROJECT_ID, GCP_LOCATION, DOCAI_PROCESSOR_ID)
        gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type="application/pdf")
        
        request = documentai.ProcessRequest(
            name=processor_name,
            gcs_document=gcs_document,
            skip_human_review=True,
        )
        
        result = docai_client.process_document(request=request)
        document = result.document

        print("--- Document AI Processing Successful ---")
        
        # Prepare data for Firestore
        doc_data = {
            "text": document.text,
            "entities": [{"type": entity.type_, "text": entity.mention_text} for entity in document.entities],
            "gcs_path": gcs_uri,
        }

        # Save to Firestore
        firestore_doc_name = file_name.replace(".pdf", "")
        firestore_ref = firestore_client.collection(FIRESTORE_COLLECTION).document(firestore_doc_name)
        firestore_ref.set(doc_data)
        
        print(f"--- Successfully saved processed data to Firestore collection '{FIRESTORE_COLLECTION}' ---")

    except Exception as e:
        print(f"\n--- An Error Occurred ---")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        # Depending on the error, you might want to add retry logic or move the file to an error bucket.
