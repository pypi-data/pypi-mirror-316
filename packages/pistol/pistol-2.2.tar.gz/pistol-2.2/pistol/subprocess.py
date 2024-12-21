import subprocess

from .logging import error

def subprocess_run(command: list[str]):
    try:
        subprocess.run(command)
    except Exception as exc:
        error(f"solo: {exc}")