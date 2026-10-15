
import httpx
from urllib.parse import urlparse
from langchain_core.tools import tool


@tool
def visit_url(url: str) -> str:
    """Visit a public webpage and return its HTML content."""

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return "Error: Please provide a valid HTTP or HTTPS URL."

    hostname = parsed.hostname.lower()

    if hostname == "localhost" or hostname.endswith(".localhost"):
        return "Error: Local URLs are not allowed."

    try:
        with httpx.Client(
            timeout=15.0,
            follow_redirects=False,
        ) as client:
            response = client.get(
                url,
                headers={"User-Agent": "VixiBot/1.0"},
            )

            if 300 <= response.status_code < 400:
                return "Redirect detected. Visit the destination URL separately."

            response.raise_for_status()

            content_type = response.headers.get("content-type", "")

            if not any(
                kind in content_type.lower()
                for kind in ("text/html", "text/plain")
            ):
                return f"Unsupported content type: {content_type}"

            if len(response.content) > 1_000_000:
                return "Error: Webpage is too large (maximum 1 MB)."

            return response.text

    except httpx.HTTPError as exc:
        return f"Error visiting URL: {exc}"
