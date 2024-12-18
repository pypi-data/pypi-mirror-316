import warnings
from pathlib import Path

import typer
from rich.console import Console

from cruxctl.command_groups.auth.auth_utilities import validate_profile
from typing_extensions import Annotated
from cruxctl.common.typer_constants import PROFILE_OPTION
import os
import yaml
from cruxctl.common.utils.api_utils import (
    get_user_info_by_token,
    set_api_token,
    read_config_file,
    get_config_file_path,
)
from cruxctl.command_groups.auth.auth_utilities import ProfileEnum
from cruxctl.command_groups.profile.profile import (
    get_current_profile,
    unset_active_profile_in_env,
    load_active_profile_env_file,
    PROFILE_ENV_VAR,
)

app = typer.Typer()

console = Console()

warnings.filterwarnings("ignore")

env_url_map = {
    ProfileEnum.DEV: "https://app.dev.cruxdata.com/settings/api-keys",
    ProfileEnum.STAGING: "https://app.stg.cruxdata.com/settings/api-keys",
    ProfileEnum.PROD: "https://app.cruxdata.com/settings/api-keys",
}
control_plane_url_map = {
    ProfileEnum.DEV: "https://api.dev.cruxinformatics.com",
    ProfileEnum.STAGING: "https://api.stg.cruxinformatics.com",
    ProfileEnum.PROD: "https://api.cruxinformatics.com",
}


@app.command("whoami")
def check_auth(
    profile: Annotated[str, PROFILE_OPTION] = None,
):
    """
    Check if the CLI is authenticated.
    """
    if not profile:
        profile = get_current_profile()
    token = set_api_token(console, profile)
    user_profile = get_user_info_by_token(token, profile)
    if user_profile:
        console.print("[green]Authenticated[/green]")
        console.print(user_profile)
    else:
        console.print("[red]Not authenticated[/red]")
        console.print("Please run 'cruxctl auth login' first.")


@app.command("login")
def authenticate_cli(
    profile: Annotated[str, PROFILE_OPTION] = None,
):
    """
    Configure the CLI with your Crux API token.
    Choose one of 3 profiles - dev, stg, prod.
    """
    # If not found, direct the user to https://app.dev.cruxdata.com/settings/api-keys

    # Interactively accept the control plane URL from
    # the user or default to https://api.cruxinformatics.com
    if not profile:
        load_active_profile_env_file()
        current_profile = os.getenv(PROFILE_ENV_VAR)
        if not current_profile:
            console.print("[red]No profile set. Defaulting to prod. ")
            profile = ProfileEnum.PROD.value
        else:
            profile = current_profile

    validate_profile(profile)
    console.print(f"Configuring CLI for {profile} profile")
    control_plane_url = control_plane_url_map.get(profile)
    if not control_plane_url:
        console.print(
            "[red]Control plane URL not found."
            "Please make sure profile is either dev, stg or prod[/red]"
        )
        raise typer.Exit(code=1)

    console.print(
        f"Please visit {env_url_map.get(profile, 'https://app.cruxdata.com/settings/api-keys')}",
        " to get your API token",
    )

    # Interactively accept the token from the user and save to the config.yaml
    api_token = console.input("Enter your CRUX API token: ")
    config = read_config_file()

    # If the token is already present, prompt the user to overwrite the token
    if config and profile in config:
        if api_token == config[profile]["CRUX_API_TOKEN"]:
            overwrite = console.input("Token already exists. Overwrite? (y/n): ")
            if overwrite.lower() != "y":
                return

    config[profile] = {}
    config[profile]["CRUX_API_TOKEN"] = api_token
    config[profile]["CONTROL_PLANE_URL"] = control_plane_url
    config_file_path = get_config_file_path()
    os.makedirs(Path(config_file_path).parent, exist_ok=True)
    with open(config_file_path, "w") as file:
        yaml.safe_dump(config, file)

    console.print("[green]API token saved successfully[/green]")


@app.command("logout")
def logout(
    profile: Annotated[str, PROFILE_OPTION] = None,
):
    """
    Remove the API token from the config file and environment variables.
    """
    unset_active_profile: bool = False
    if not profile:
        profile = get_current_profile()
        unset_active_profile = True
    elif profile == get_current_profile():
        unset_active_profile = True

    config = read_config_file()
    if config and profile in config:
        del config[profile]
        config_file_path = get_config_file_path()
        with open(config_file_path, "w") as file:
            yaml.safe_dump(config, file)

        if unset_active_profile:
            unset_active_profile_in_env()
        console.print(f"[green]Logged out successfully for profile {profile}[/green]")
    else:
        console.print(
            f"[red]Not logged in. No API token found for this profile:{profile}[/red]"
        )
