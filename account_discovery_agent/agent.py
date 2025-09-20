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

import logging
import re

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import google_search
from google.genai import types as genai_types

from common.config import config


def citation_replacement_callback(
    callback_context: CallbackContext,
) -> genai_types.Content:
    """Appends a formatted list of sources to the agent's response."""
    session = callback_context._invocation_context.session
    final_response = ""
    # Find the last agent response event to get the text and grounding.
    for event in reversed(session.events):
        if (
            event.author == callback_context._invocation_context.agent.name
            and event.is_final_response()
        ):
            final_response = event.content.parts[0].text if event.content.parts else ""
            grounding_metadata = event.grounding_metadata
            break
    else:
        return None  # Should not happen if the agent produced a response.

    sources = []
    if grounding_metadata:
        for chunk in grounding_metadata.grounding_chunks:
            if hasattr(chunk, "web") and chunk.web and chunk.web.uri:
                sources.append(
                    {"uri": chunk.web.uri, "title": chunk.web.title}
                )

    # Append the sources to the final report
    output = f"# Discovery Report\n\n{final_response}"
    output += "\n\n---\n\n## Sources\n"

    if not sources:
        output += "No web sources were cited for this report."
    else:
        for i, source in enumerate(sources):
            title = source.get("title", "").strip() or source.get("uri")
            output += f"{i+1}. [{title}]({source.get('uri')})\n"

    # Return a new Content object to replace the original agent output
    return genai_types.Content(parts=[genai_types.Part(text=output)])


# --- AGENT DEFINITION ---
# This agent is adapted from the Python code provided from AI Studio.
# root_agent = LlmAgent(
#     model=config.worker_model,
#     name="account_discovery_agent",
#     description="Performs a deep analysis of a company based on its website.",
#     instruction='''You are an expert business analyst and account discovery agent. Your task is to perform a deep analysis of the company at the website: {url}.
#
# Provide a comprehensive report in well-structured Markdown format.
#
# Specifically, I need you to focus on the following key areas:
# {selected_prompts}
#
# In addition to the above, please address the following specific instructions:
# "{custom_instructions}"
#
# Begin your analysis now. Ensure your report is detailed, insightful, and directly based on the information available from your search.
# ''',
#     tools=[google_search],
#     after_agent_callback=citation_replacement_callback,
# )
from account_discovery_agent.smart_chat_agent import create_smart_chat_agent

root_agent = create_smart_chat_agent()
