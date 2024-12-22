import json
import logging
import os
from typing import List

import toml
from rich.console import Console
from rich.prompt import Prompt

from uhugo.post_install.detect_providers import Provider

log = logging.getLogger(__name__)


class UpdateProvider:
    """
    Update providers with Hugo version
    """

    def __init__(self, providers: List[Provider], console: Console, version: str):
        """
        :param providers: List of Provider objects
        :param console: Rich Console object
        :param version: Hugo version
        """
        self.providers = providers
        self.console = console
        self.version = version

    def update(self):
        """
        Update providers with Hugo version
        """
        _providers = {
            "netlify": True,
            "vercel": True,
            "cloudflare": True,
        }
        for provider in self.providers:
            if provider.name == "netlify":
                _providers[provider.name] = self.update_netlify(provider)
            elif provider.name == "vercel":
                _providers[provider.name] = self.update_vercel(provider)
            elif provider.name == "cloudflare":
                _providers[provider.name] = self.update_cloudflare(provider)

        failed_providers = _providers.items()

        if len(failed_providers) > 0:
            for provider, status in _providers.items():
                if not status:
                    self.console.print(f"\n{provider} provider(s) not updated to {self.version} :x:", style="red bold")
            return
        self.console.print(f"\nAll providers updated to {self.version} :tada:", style="green bold")

    def update_netlify(self, provider: Provider) -> bool:
        """
        Update Netlify provider with a latest Hugo variables

        :param provider: Provider object
        :return: False if not updated
        """
        try:
            with open(provider.path, "r+") as f:
                data = toml.load(f)
                if data["context"]["production"]["environment"]["HUGO_VERSION"] == self.version:
                    self.console.print(
                        ":heavy_check_mark: Netlify - Hugo version is already up to date", style="green bold"
                    )
                    return True
                data["context"]["production"]["environment"]["HUGO_VERSION"] = self.version
                data["context"]["deploy-preview"]["environment"]["HUGO_VERSION"] = self.version
                f.seek(0)
                toml.dump(data, f)
                f.truncate()
            self.console.print(":heavy_check_mark: Netlify", style="green bold")
            return True
        except FileNotFoundError as e:
            log.debug(e)
            self.console.print(f":x: Netlify - File '{provider.path}' not found", style="bold red")
            return False

    def update_vercel(self, provider: Provider) -> bool:
        """
        Update Vercel provider with a latest Hugo variables

        :param provider: Provider object
        :return: False if not updated
        """

        try:
            with open(provider.path, "r+") as f:
                json_data = json.load(f)
                if json_data["build"]["env"]["HUGO_VERSION"] == self.version:
                    self.console.print(
                        ":heavy_check_mark: Vercel - Hugo version is already up to date", style="green bold"
                    )
                    return True
                json_data["build"]["env"]["HUGO_VERSION"] = self.version
                f.seek(0)
                json.dump(json_data, f, indent=4)
                f.truncate()
            self.console.print(":heavy_check_mark: Vercel", style="green bold")
            return True
        except FileNotFoundError as e:
            log.debug(e)
            self.console.print(f":x: Vercel - File '{provider.path}' not found", style="bold red")
            return False

    def update_cloudflare(self, provider: Provider) -> bool:
        """
        Update Cloudflare provider with a latest Hugo variables

        :param provider: Provider object
        :return: False if not updated
        """

        # Get the environment variables from the config file
        for key, val in provider.model_dump().items():
            if val and val.startswith("env"):
                try:
                    setattr(provider, key, os.environ[val.split(":")[1]])
                except KeyError as e:
                    log.debug(e)
                    self.console.print(f"Environment variable '{val.split(':')[1]}' not found", style="bold red")
                    return False

        from ..post_install.providers.cloudflare import Cloudflare

        cf = Cloudflare(provider.api_key, provider.email_address, provider.account_id, self.version)
        projects = cf.get_projects(provider.project).json()
        # TODO: Stop spinner before continuing or else this will not show up
        if projects["success"] and isinstance(projects["result"], list):
            names = [name["name"] for name in projects["result"]]
            name = Prompt.ask("Enter project name", choices=names)
        elif not projects["success"]:
            self.console.print("There was an error fetching your Cloudflare project", style="bold red")
            log.debug(projects)
            return False
        else:
            name = provider.project

        current_version = cf.current_version(name)
        if current_version != self.version:
            log.debug(f"Current Hugo version in Cloudflare: v{current_version}")
        else:
            self.console.print(":heavy_check_mark: Cloudflare - Hugo version is already up to date", style="green bold")
            return False

        response = cf.update_api(name).json()
        if not response["success"]:
            self.console.print("There was an error updating your Cloudflare environment")
            log.debug(response)
            return False
        self.console.print(":heavy_check_mark: Cloudflare", style="green bold")
        return True
