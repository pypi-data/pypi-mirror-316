
def print_verbose(message: str, verbose: bool=True) -> None:
    """
    Print a message if verbose is True.
    
    Parameters:
        message (str): The message to print.
        verbose (bool): If True, the message will be printed.
    """
    if verbose:
        print(str(message))