from .messages import print_verbose
import pathlib

def sql_quotename(name: str=None, brackets: bool=True, ticks: bool=False, verbose: bool=False) -> str|None:
    """
    Quote a SQL Server name string.
    Parameters:
        name (str): The name to quote.
        brackets (bool): Whether to use brackets.
    Returns:
        str: The quoted name.
    """
    if name is None:
        print_verbose("No name provided; exiting sql_quotename.", verbose)
        exit
    return_value = f"{name.replace('[','').replace(']','')}"
    if brackets:
        return_value = f"[{return_value}]"
    if ticks or not brackets:
        return_value = f"'{return_value}'"
    return return_value

def pathing(input: str | pathlib.Path, verbose: bool=False) -> pathlib.Path|None:
    """
    Standardize a path string.
    Parameters:
        path (str): The path to standardize.
    Returns:
        str: The standardized path.
    """
    if input is None:
        print_verbose("No path provided; exiting pathing.", verbose)
        exit
    if isinstance(input, str):
        input.replace('\\','/')
        input = pathlib.Path(input)
    else:
        input = input
    if input.exists():
        return input
    else:
        print_verbose(f"Path {input} does not exist; exiting pathing.", verbose)
        exit