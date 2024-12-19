import os
import tempfile
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def pull(url):
    """
    Pulls from an HTTP(S) URL
    """
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,  # Time between retries: 1, 2, 4, 8 seconds, etc.
        status_forcelist=[500, 502, 503, 504], # Retry on server errors
        allowed_methods=["GET"],
    )

    # Create a named temporary file with the .tar.gz extension
    temp_file = tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False)

    # Create a session and mount the retry-enabled adapter
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        with session.get(url, stream=True) as response:
            response.raise_for_status()  # Raise exception for HTTP errors
            with open(temp_file.name, "wb") as output_file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Write non-empty chunks to file
                        output_file.write(chunk)
        return temp_file.name
    except Exception:
        # Clean up on errors
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
        raise
