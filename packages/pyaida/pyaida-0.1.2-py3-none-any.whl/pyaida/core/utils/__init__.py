"""some convenience methods that we can break out later"""

from loguru import logger
import datetime
from datetime import timezone
import hashlib
import uuid
import json
import requests
from .dates import utc_now, now


def batch_collection(collection, batch_size):
    """Yield successive batches of size batch_size from collection. can also be used to chunk string of chars"""
    for i in range(0, len(collection), batch_size):
        yield collection[i : i + batch_size]


def short_md5_hash(input_string: str, length: int = 8) -> str:
    """
    Generate a short hash of a string using MD5 and truncate to the specified length.

    Args:
        input_string (str): The input string to hash.
        length (int): The desired length of the hash (default is 8).

    Returns:
        str: A short MD5 hash of the input string with the specified length.
    """
    if length < 1 or length > 32:
        raise ValueError("Length must be between 1 and 32 characters.")

    return hashlib.md5(input_string.encode()).hexdigest()[:length]


def sha_hash(input_str: str | dict):
    """"""

    if isinstance(input_str, dict):
        input_str = json.dumps(input_str)

    namespace = uuid.NAMESPACE_DNS  # Predefined namespace for domain names
    return str(uuid.uuid5(namespace, input_str))


def load_secret(key: str):
    """TODO: load secrete from env or otherwise"""
    return "test" if key == "test" else None


def call_api(
    endpoint, verb="get", api_host=None, data=None, token_key: str = None, **kwargs
):
    """

    convenience to wrap rest calls with tokens and mapping of kwargs

    """

    api_host = api_host or "http://localhost:8000"

    token = load_secret(token_key or "test")
    headers = {
        "Content-type": "application/json",
    }
    if token:
        headers.update(
            {
                "Authorization": f"Bearer {token}",
            }
        )
    f = getattr(requests, verb)

    """rewrite the url with the kwargs"""
    endpoint = endpoint.format_map(kwargs)

    if verb == "post":
        """some flexibility on how to call this - although we may not want to rewrite in this case ^"""
        if data is None:
            data = kwargs
        if not isinstance(data, str):
            """the case of pydantic models"""
            if hasattr(data, "model_dump"):
                data = data.model_dump()
            data = json.dumps(data)

    response = f(
        f"{api_host}/{endpoint.lstrip('/')}",
        headers=headers,
        params=kwargs,
        data=data,
    )

    try:
        return {"data": response.json(), "type": "json", "status": response.status_code}
    except:
        return {
            "data": response.content,
            "type": response.headers.get("Content-Type"),
            "status": response.status_code,
        }
