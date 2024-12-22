import requests 
from .messages import print_verbose

def get(url: str, verbose: bool = False, **kwargs) -> dict:
    """Get JSON data from a URL."""
    try:
        response = requests.get(url, **kwargs)
        return response.json()
    except requests.exceptions.RequestException as e:
        print_verbose(f"Error: {e}", verbose=verbose)