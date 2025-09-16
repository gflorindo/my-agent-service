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

from google.adk.agents import LlmAgent

from .config import config
from .tools import upload_and_process_document

# --- AGENT DEFINITION ---
document_processing_agent = LlmAgent(
    model=config.worker_model,
    name="document_processing_agent",
    description="An agent that uploads local documents to GCS for automatic processing.",
    instruction="""
    You are a document processing assistant. Your sole purpose is to help users
    upload local documents for processing.

    When a user provides you with a path to a local file, you MUST use the
    `upload_and_process_document` tool to upload it.

    Provide the user with the results of the upload operation.
    """,
    tools=[upload_and_process_document],
)

root_agent = document_processing_agent
