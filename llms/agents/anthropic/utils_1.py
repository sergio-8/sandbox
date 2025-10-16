import mimetypes
import os
import re
import base64
import logging
import io

# === Third-Party ===
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai  # Keep only Google
from IPython.display import HTML, display
from typing import Any

# === Env & Clients ===
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Google Gemini client if API key is present
if google_api_key:
    try:
        genai.configure(api_key=google_api_key)
        logging.info("Google Gemini client configured successfully.")
    except Exception as e:
        logging.error(f"Failed to configure Google Gemini: {e}")
else:
    logging.warning(
        "GOOGLE_API_KEY not found. Gemini models will not be available."
    )


def get_response(model: str, prompt: str) -> str:
    """
    Get a text response from a Google Gemini model.
    """

    if not google_api_key:
        logging.error("Google API key not configured. Cannot make API call.")
        raise ValueError("GOOGLE_API_KEY not found.")

    try:
        model_client = genai.GenerativeModel(model_name=model)
        response = model_client.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Google Gemini API call failed for model {model}: {e}")
        # Re-raise the exception to signal failure
        raise e


# === Data Loading ===
def load_and_prepare_data(csv_path: str) -> pd.DataFrame:
    """Load CSV and derive date parts commonly used in charts."""
    df = pd.read_csv(csv_path)
    # Be tolerant if 'date' exists
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["quarter"] = df["date"].dt.quarter
        df["month"] = df["date"].dt.month
        df["year"] = df["date"].dt.year
    return df


# === Helpers ===
def make_schema_text(df: pd.DataFrame) -> str:
    """Return a human-readable schema from a DataFrame."""
    return "\n".join(f"- {c}: {dt}" for c, dt in df.dtypes.items())


def ensure_execute_python_tags(text: str) -> str:
    """Normalize code to be wrapped in <execute_python>...</execute_python>."""
    text = text.strip()
    # Strip ```python fences if present
    text = re.sub(r"^```(?:python)?\s*|\s*```$", "", text).strip()
    if "<execute_python>" not in text:
        text = f"<execute_python>\n{text}\n</execute_python>"
    return text


def encode_image_b64(path: str) -> tuple[str, str]:
    """Return (media_type, base64_str) for an image file path."""
    mime, _ = mimetypes.guess_type(path)
    media_type = mime or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return media_type, b64


def print_html(content: Any, title: str | None = None, is_image: bool = False):
    """
    Pretty-print inside a styled card.
    - If is_image=True and content is a string: treat as image path/URL and render <img>.
    - If content is a pandas DataFrame/Series: render as an HTML table.
    - Otherwise (strings/others): show as code/text in <pre><code>.
    """
    try:
        from html import escape as _escape
    except ImportError:
        _escape = lambda x: x

    def image_to_base64(image_path: str) -> str:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    # Render content
    if is_image and isinstance(content, str):
        b64 = image_to_base64(content)
        rendered = f'<img src="data:image/png;base64,{b64}" alt="Image" style="max-width:100%; height:auto; border-radius:8px;">'
    elif isinstance(content, pd.DataFrame):
        rendered = content.to_html(
            classes="pretty-table", index=False, border=0, escape=False
        )
    elif isinstance(content, pd.Series):
        rendered = content.to_frame().to_html(
            classes="pretty-table", border=0, escape=False
        )
    elif isinstance(content, str):
        rendered = f"<pre><code>{_escape(content)}</code></pre>"
    else:
        rendered = f"<pre><code>{_escape(str(content))}</code></pre>"

    css = """
    <style>
    .pretty-card{
      font-family: ui-sans-serif, system-ui;
      border: 2px solid transparent;
      border-radius: 14px;
      padding: 14px 16px;
      margin: 10px 0;
      background: linear-gradient(#fff, #fff) padding-box,
                  linear-gradient(135deg, #3b82f6, #9333ea) border-box;
      color: #111;
      box-shadow: 0 4px 12px rgba(0,0,0,.08);
    }
    .pretty-title{
      font-weight:700;
      margin-bottom:8px;
      font-size:14px;
      color:#111;
    }
    /* 🔒 Only affects INSIDE the card */
    .pretty-card pre, 
    .pretty-card code {
      background: #f3f4f6;
      color: #111;
      padding: 8px;
      border-radius: 8px;
      display: block;
      overflow-x: auto;
      font-size: 13px;
      white-space: pre-wrap;
    }
    .pretty-card img { max-width: 100%; height: auto; border-radius: 8px; }
    .pretty-card table.pretty-table {
      border-collapse: collapse;
      width: 100%;
      font-size: 13px;
      color: #111;
    }
    .pretty-card table.pretty-table th, 
    .pretty-card table.pretty-table td {
      border: 1px solid #e5e7eb;
      padding: 6px 8px;
      text-align: left;
    }
    .pretty-card table.pretty-table th { background: #f9fafb; font-weight: 600; }
    </style>
    """

    title_html = f'<div class="pretty-title">{title}</div>' if title else ""
    card = f'<div class="pretty-card">{title_html}{rendered}</div>'
    display(HTML(css + card))


def image_google_call(
        model_name: str, prompt: str, media_type: str, b64: str
) -> str:
    """
    Call Google Gemini (GenerativeModel) with text+image and return the text response.
    Adds a system message to enforce strict JSON output.
    Note: media_type is unused by PIL but kept for signature consistency.
    """
    if not google_api_key:
        logging.warning(
            "GOOGLE_API_KEY not found. Skipping Google Gemini image call."
        )
        raise ValueError(
            "Google API key not configured. Cannot make image call."
        )

    try:
        # 1. Initialize the model with the system prompt
        # Use a model that supports vision (e.g., 'gemini-1.5-pro')
        model_client = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=(
                "You are a careful assistant. Respond with a single valid JSON object only. "
                "Do not include markdown, code fences, or commentary outside JSON."
            ),
        )

        # 2. Prepare the image from base64 bytes
        image_bytes = base64.b64decode(b64)
        # Use io.BytesIO to treat the bytes as a file-like object
        image_pil = Image.open(io.BytesIO(image_bytes))

        # 3. Call the API with a list of content parts
        # The genai SDK natively understands PIL Image objects
        response = model_client.generate_content([prompt, image_pil])

        # 4. Parse and return the text response
        return response.text

    except Exception as e:
        logging.error(
            f"Google Gemini image call failed for model {model_name}: {e}"
        )
        raise e  # Re-raise to be consistent