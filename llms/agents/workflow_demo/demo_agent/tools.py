"""Tools for the Demo agent."""

import os
from typing import Any, Dict

from google import auth
from google.adk.tools import tool_context as tool_context_lib
import google.auth.transport.requests
import html
import requests

ToolContext = tool_context_lib.ToolContext
default = auth.default

# pylint: disable=g-import-not-at-top
if os.environ.get("IMPORT_FROM_xxx"):
    from xxx.cloud.ml.discoveryengine.agents.cloudia.cloudia import get_flags
else:
    from . import get_flags

# Search API call vars
ENDPOINT = "https://discoveryengine.googleapis.com"
STAGING_ENDPOINT = "https://staging-discoveryengine-googleapis.sandbox.google.com"
ANSWER_API = f"{ENDPOINT}/v1alpha/projects/{get_flags.PROJECT}/locations/global/collections/default_collection/engines/{get_flags.ENGINE_ID}/servingConfigs/default_search:answer"


def format_json_to_html(json_data: Dict[str, Any]) -> str:
    """
    Generates HTML text from JSON data response of VAIS answer endpoint containing an answer, citations, and references.
    Args:
        json_data (Dict[str, Any]): A dictionary containing the JSON data.

    Returns:
        str: The generated HTML text.
    """

    answer_data = json_data.get("answer", {})
    answer_text = answer_data.get("answerText", "")
    citations = answer_data.get("citations", [])
    references_list = answer_data.get("references", [])

    if not answer_text:
        return "<p>No data to format.</p>"  # Return simple HTML for no data

    reference_map = {}
    for i, ref in enumerate(references_list):
        uri = None
        title = None
        if "chunkInfo" in ref and ref["chunkInfo"].get("documentMetadata"):
            uri = ref["chunkInfo"]["documentMetadata"].get("uri")
            title = ref["chunkInfo"]["documentMetadata"].get("title", "Source")
        elif "structuredDocumentInfo" in ref:
            uri = ref["structuredDocumentInfo"].get("uri")
            title = ref["structuredDocumentInfo"].get("title", "Source")
        if uri:
            reference_map[str(i)] = {"uri": uri, "title": title}

    processed_citations = []
    for c in citations:
        # Default startIndex to 0 if missing
        start_index = int(c.get("startIndex", 0))
        end_index = c.get("endIndex")
        if end_index is None:
            print(f"Warning: Citation missing endIndex, skipping: {c}")
            continue
        end_index = int(end_index)
        processed_citations.append({
            "startIndex": start_index,
            "endIndex": end_index,
            "sources": c.get("sources", [])
        })

    processed_citations.sort(key=lambda c: c["startIndex"])

    html_parts = []
    current_pos = 0

    for citation in processed_citations:
        start_index = citation["startIndex"]
        end_index = citation["endIndex"]
        sources = citation["sources"]

        if start_index > current_pos:
            html_parts.append(html.escape(answer_text[current_pos:start_index]))

        cited_text_segment = html.escape(answer_text[start_index:end_index + 1])

        if cited_text_segment:
            segment_length = len(cited_text_segment)
            last_character = cited_text_segment[segment_length - 1]
            cited_text_segment = cited_text_segment[:segment_length - 1]

        html_parts.append(cited_text_segment)

        citation_links_html = []
        for source in sources:
            ref_id = source.get("referenceId")
            if ref_id in reference_map:
                ref_details = reference_map[ref_id]
                escaped_uri = html.escape(ref_details['uri'])
                link_text = str(int(ref_id) + 1)
                escaped_title = html.escape(ref_details.get('title', f"Source {link_text}"))
                citation_links_html.append(
                    f'<a href="{escaped_uri}" title="{escaped_title}" target="_blank" rel="noopener noreferrer">{link_text}</a>')

            else:
                citation_links_html.append(html.escape(f"[Ref {int(ref_id) + 1} not found]"))

        if citation_links_html:
            html_parts.append(f" {', '.join(citation_links_html)} ")
            html_parts.append(last_character)

        current_pos = end_index + 1

    if current_pos < len(answer_text):
        html_parts.append(html.escape(answer_text[current_pos:]))
    return "".join(html_parts)


def format_json_to_markdown(json_data: Dict[str, Any]) -> str:
    """
    Generates Markdown text from JSON data response of VAIS answer endpoint containing an answer, citations, and references.
    Args:
        json_data (Dict[str, Any]): A string containing the JSON data.

    Returns:
        str: The generated Markdown text.
    """

    answer_data = json_data.get("answer", {})
    answer_text = answer_data.get("answerText", "")
    citations = answer_data.get("citations", [])
    references_list = answer_data.get("references", [])

    if not answer_text:
        return "No data to format."

    reference_map = {}
    for i, ref in enumerate(references_list):
        uri = None
        title = None
        if "chunkInfo" in ref and ref["chunkInfo"].get("documentMetadata"):
            uri = ref["chunkInfo"]["documentMetadata"].get("uri")
            title = ref["chunkInfo"]["documentMetadata"].get("title", "Source")
        elif "structuredDocumentInfo" in ref:
            uri = ref["structuredDocumentInfo"].get("uri")
            title = ref["structuredDocumentInfo"].get("title", "Source")
        if uri:
            reference_map[str(i)] = {"uri": uri, "title": title}

    processed_citations = []
    for c in citations:
        # Default startIndex to 0 if missing
        start_index = int(c.get("startIndex", 0))
        end_index = c.get("endIndex")
        if end_index is None:
            print(f"Warning: Citation missing endIndex, skipping: {c}")
            continue
        end_index = int(end_index)
        processed_citations.append({
            "startIndex": start_index,
            "endIndex": end_index,
            "sources": c.get("sources", [])
        })

    processed_citations.sort(key=lambda c: c["startIndex"])

    markdown_parts = []
    current_pos = 0

    for citation in processed_citations:
        start_index = citation["startIndex"]
        end_index = citation["endIndex"]
        sources = citation["sources"]

        if start_index > current_pos:
            markdown_parts.append(answer_text[current_pos:start_index])

        cited_text_segment = answer_text[start_index:end_index + 1]
        markdown_parts.append(cited_text_segment)

        citation_links = []
        for source in sources:
            ref_id = source.get("referenceId")
            if ref_id in reference_map:
                ref_details = reference_map[ref_id]
                citation_links.append(f"[{int(ref_id) + 1}]({ref_details['uri']})")
            else:
                citation_links.append(f"[Ref {int(ref_id) + 1} not found]")
        if citation_links:
            markdown_parts.append(f" ({', '.join(citation_links)})")

        current_pos = end_index + 1

    if current_pos < len(answer_text):
        markdown_parts.append(answer_text[current_pos:])

    return " ".join(markdown_parts)


def authenticate_user(key: str, tool_context: ToolContext):  # pylint: disable=redefined-outer-name
    """Authenticates the user and updates the token in the state memory."""
    creds, _ = default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    update_state(key, creds.token, tool_context)


def update_state(key: str, value: str, tool_context: ToolContext):  # pylint: disable=redefined-outer-name
    """Updates the current key / value pair in the state memory.

    Args:
        key (str): The key to update.
        value (str): The value to update.
        tool_context (ToolContext): The tool context containing the state of the
            tool.

    Returns:
        str: The updated value.
    """
    tool_context.state[key] = value
    return value


def get_state(key: str, tool_context: ToolContext) -> str:  # pylint: disable=redefined-outer-name
    """Gets the current key / value pair in the state memory.

    Args:
        key (str): The key to retrieve.
        tool_context (ToolContext): The tool context containing the state of the
            tool.

    Returns:
        str: The value associated with the key, or None if not found.
    """
    return tool_context.state.get(key, None)


def get_answer_results(query: str, token: str) -> str:
    """Calls the Agentspace search API to retrieve relevant information.

    Args:
        query (str): The user's query.
        token (str): The authentication token.
    Returns:
        str: The search response from the API.
    """
    response = requests.post(
        ANSWER_API,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        },
        json={
            "query": {"text": query},
            "answerGenerationSpec": {"includeCitations": True},
        },
    )
    if response.status_code != 200:
        return response.json()
    return format_json_to_html(response.json())


if __name__ == "__main__":
    credentials, _ = default()
    credentials.refresh(google.auth.transport.requests.Request())
    print(
        get_answer_results(
            "what is agentspace?", credentials.token
        )
    )
