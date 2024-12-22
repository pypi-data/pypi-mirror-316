import sys
from collections import deque


def tail(filename=None, n=None, c=None):
    """
    Mimics the Unix `tail` command, with support for piped content.

    Parameters:
        filename (str, optional): Path to the file to read. If None, reads from stdin.
        n (int, optional): Number of lines to display. Default is 10 if not specified.
        c (int, optional): Number of bytes to display. Overrides `n` if specified.
    """
    try:
        if filename:
            source = open(filename, "rb" if c else "r")
        else:
            source = sys.stdin

        with source as file:
            if c:
                content = file.read()
                print(
                    content[-c:]
                    if isinstance(content, str)
                    else content.decode("utf-8", errors="replace")[-c:]
                )
            else:
                lines = deque(
                    file if filename else iter(file.readline, ""), maxlen=n or 10
                )
                for line in lines:
                    print(line, end="")
    except Exception as e:
        print(f"Error reading file {filename}: {e}")


def tail_command(filenames=None, n=None, c=None):
    """
    Handles files or piped input with the `tail` command-like functionality.

    Parameters:
        filenames (list, optional): List of file paths. If None, reads from stdin.
        n (int, optional): Number of lines to display per file. Default is 10.
        c (int, optional): Number of bytes to display per file. Overrides `n` if specified.
    """
    if filenames:
        for filename in filenames:
            if len(filenames) > 1:
                print(f"==> {filename} <==")
            tail(filename, n=n, c=c)
            if len(filenames) > 1:
                print()
    else:
        tail(n=n, c=c)
