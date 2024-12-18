"""Handles enabling custom flags by name or uid"""

import click

import spyctl.config.configs as cfg
import spyctl.spyctl_lib as lib
from spyctl import cli
from spyctl.api.custom_flags import get_custom_flags, put_enable_custom_flag


@click.command("custom-flag", cls=lib.CustomCommand, epilog=lib.SUB_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.argument("name_or_id", required=True)
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    help="Automatically answer yes to all prompts.",
)
def enable_custom_flag(name_or_id, **kwargs):
    """Enable a custom flag by name or uid."""
    yes_option = kwargs.pop("yes")
    if yes_option:
        cli.set_yes_option()
    handle_enable_custom_flag(name_or_id)


def handle_enable_custom_flag(name_or_id):
    """
    Enables a custom flag based on the provided name or UID.

    Args:
        name_or_id (str): The name or UID of the custom flag to be enabled.

    Returns:
        None
    """
    ctx = cfg.get_current_context()
    params = {"name_or_uid_contains": name_or_id, "page_size": -1}
    custom_flags, _ = get_custom_flags(*ctx.get_api_data(), **params)
    if len(custom_flags) == 0:
        cli.err_exit(f"No custom flags matching name_or_uid '{name_or_id}'")
    for custom_flag in custom_flags:
        name = custom_flag["name"]
        uid = custom_flag["uid"]
        perform_enable = cli.query_yes_no(
            f"Are you sure you want to enable custom flag '{name} - {uid}'?"
        )
        if perform_enable:
            put_enable_custom_flag(
                *ctx.get_api_data(),
                uid,
            )
            cli.try_log(f"Successfully enabled custom flag '{name} - {uid}'")
        else:
            cli.try_log(f"Skipping enable of '{name} - {uid}'")
