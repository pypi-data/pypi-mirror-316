import os
from pathlib import Path
from typing import Union, List

from pydantic import BaseModel

HERE = os.getcwd()


class Provider(BaseModel):
    """
    This holds the information about the provider
    """

    name: Union[str, None] = None
    project: Union[str, None] = None
    file_name: Union[str, None] = None
    api_key: Union[str, None] = None
    account_id: Union[str, None] = None
    email_address: Union[str, None] = None
    path: Union[str, None] = None


def check_hugo_file() -> Provider:
    """
    Checks for ``config.yaml`` or ``config.toml``, if exists then it checks for ``uhugo`` key

    :return Provider: An object with ``name`` and ``file_name``
    """

    path = Path(HERE, "config.toml")
    if not path.exists():
        path = Path(HERE, "config.yaml")
        if not path.exists():
            return Provider()
        else:
            import yaml

            try:
                from yaml import CLoader as Loader, CDumper as Dumper
            except ImportError:
                from yaml import Loader, Dumper
            with open(path) as f:
                data = yaml.load(f, Loader=Loader)
    else:
        import toml

        with open(path) as f:
            data = toml.load(f)

    return Provider(**data["uhugo"])


def check_providers_fs() -> List[Provider]:
    """
    Checks file system for any providers that matches the list

    :return: A Provider
    """

    files = ["netlify.yaml", "vercel.json", "netlify.toml"]
    providers: List[Provider] = []

    for file in files:
        path = Path(HERE, file)
        if path.exists():
            providers.append(Provider(**{"name": path.name.split(".")[0], "path": path.__str__()}))

    return providers
