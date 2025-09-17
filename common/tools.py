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

import mimetypes
import os
from io import BytesIO

from google.cloud import storage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def upload_and_process_document(file_path: str) -> dict:
    """Uploads a local document to GCS to trigger the processing pipeline.

    This tool automatically detects the document's content type and uploads it
    to the configured GCS bucket. The bucket is monitored by a service that
    will automatically process the document using Document AI and index its
    contents in Firestore.

    Supports various file types including PDF, DOCX, PPTX, PNG, JPEG, and more.

    Args:
        file_path (str): The local path to the document file.

    Returns:
        dict: A dictionary containing the status and the GCS path of the uploaded file.
    """
    bucket_name = os.environ.get("STORAGE_BUCKET_NAME")
    if not bucket_name:
        return {
            "status": "error",
            "message": "STORAGE_BUCKET_NAME environment variable is not set.",
        }

    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found at: {file_path}"}

    try:
        # Guess the content type of the file
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"  # Default content type

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        gcs_file_name = os.path.basename(file_path)
        blob = bucket.blob(gcs_file_name)

        blob.upload_from_filename(file_path, content_type=content_type)

        gcs_path = f"gs://{bucket_name}/{gcs_file_name}"
        return {
            "status": "success",
            "message": f"File '{gcs_file_name}' uploaded to GCS. Processing will start automatically.",
            "gcs_path": gcs_path,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def convert_and_upload_to_gcs(file_path: str, bucket_name: str) -> dict:
    """Converts a text file to PDF and uploads it to a GCS bucket.

    Args:
        file_path (str): The local path to the text file.
        bucket_name (str): The name of the GCS bucket.

    Returns:
        dict: A dictionary containing the status and the GCS path of the uploaded file.
    """
    try:
        with open(file_path, "r") as f:
            file_content = f.read()

        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        text_object = c.beginText(40, 750)
        text_object.setFont("Helvetica", 12)
        for line in file_content.splitlines():
            text_object.textLine(line)
        c.drawText(text_object)
        c.save()
        pdf_buffer.seek(0)

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        gcs_pdf_name = file_path.replace(".txt", ".pdf")
        blob = bucket.blob(gcs_pdf_name)
        blob.upload_from_file(pdf_buffer, content_type="application/pdf")

        gcs_path = f"gs://{bucket_name}/{gcs_pdf_name}"
        return {"status": "success", "gcs_path": gcs_path}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_source_documents(query: str) -> dict:
    """Searches for information within the private, uploaded documents.

    Args:
        query (str): The search query.

    Returns:
        dict: A dictionary containing the search results.
    """
    # This is a placeholder implementation.
    # In a real-world scenario, this would query a vector database.
    return {"status": "success", "results": f"No documents found for query: {query}"}
