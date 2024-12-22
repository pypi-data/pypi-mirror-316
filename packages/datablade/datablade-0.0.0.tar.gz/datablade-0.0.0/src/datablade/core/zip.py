import requests, zipfile, io, pathlib
from .messages import print_verbose
from .strings import pathing

def get(url:str, path:str|pathlib.Path=None, verbose:bool=False, **kwargs) -> None|io.BytesIO:
    """Download a file from a URL and save it to a path."""
    try:
        print_verbose(f"Downloading {url}", verbose=verbose)
        data = requests.get(url, **kwargs).content 
        zip_buffer = io.BytesIO(data)
        if path is None:
            return zip_buffer
        else:
            print_verbose(f"Saving data to {path}", verbose=verbose)
            zip_buffer.seek(0)
            with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                for zip_info in zip_ref.infolist():
                    extract_path = pathing(path) / zip_info.filename
                    extract_path.parent.mkdir(parents=True, exist_ok=True) 
                    with open(extract_path, 'wb') as f:
                        f.write(zip_ref.read(zip_info.filename))
                        f.close()
    except requests.exceptions.RequestException as e:
        print_verbose(f"Error: {e}", verbose=verbose)