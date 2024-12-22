from importlib.metadata import version, PackageNotFoundError
from pathlib import Path

try:
    __version__ = version("uhugo")
except PackageNotFoundError:
    __version__ = "0.0.0"

# Creates a .uhugo folder in user folder
if not Path.home().joinpath(".uhugo").is_dir():
    Path.home().joinpath(".uhugo").mkdir(exist_ok=True)
