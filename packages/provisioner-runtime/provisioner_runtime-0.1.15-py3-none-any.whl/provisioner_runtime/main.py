#!/usr/bin/env python3

import os
import pathlib

from loguru import logger

from provisioner_shared.components.runtime.cli.entrypoint import EntryPoint
from provisioner_shared.components.runtime.command.config.cli import CONFIG_USER_PATH, append_config_cmd_to_cli
from provisioner_shared.components.runtime.command.plugins.cli import append_plugins_cmd_to_cli
from provisioner_shared.components.runtime.config.domain.config import ProvisionerConfig
from provisioner_shared.components.runtime.config.manager.config_manager import ConfigManager
from provisioner_shared.components.runtime.infra.context import Context
from provisioner_shared.components.runtime.shared.collaborators import CoreCollaborators
from provisioner_shared.components.runtime.shared.globals import COMMON_COMMANDS_GROUP_NAME

CONFIG_INTERNAL_PATH = f"{pathlib.Path(__file__).parent}/resources/config.yaml"

"""
The --dry-run and --verbose flags aren't available on the pre-init phase
since logger is being set-up after Typer is initialized.
I've added pre Typer run env var to control the visiblity of components debug logs
such as config-loader, package-loader etc..
"""
ENV_VAR_ENABLE_PRE_INIT_DEBUG = "PROVISIONER_PRE_INIT_DEBUG"
debug_pre_init = os.getenv(key=ENV_VAR_ENABLE_PRE_INIT_DEBUG, default=False)

if not debug_pre_init:
    logger.remove()

app = EntryPoint.create_typer(
    title="Provision Everything Anywhere (install plugins from https://zachinachshon.com/provisioner)",
    config_resolver_fn=lambda: ConfigManager.instance().load(CONFIG_INTERNAL_PATH, CONFIG_USER_PATH, ProvisionerConfig),
)


def load_plugin(plugin_module):
    plugin_module.load_config()
    plugin_module.append_to_cli(app)


cols = CoreCollaborators(Context.createEmpty())
cols.package_loader().load_modules_fn(
    filter_keyword="provisioner",
    import_path="main",
    exclusions=["provisioner-runtime", "provisioner_runtime", "provisioner_shared", "provisioner-shared"],
    callback=lambda module: load_plugin(plugin_module=module),
    debug=debug_pre_init,
)

append_config_cmd_to_cli(app, cli_group_name=COMMON_COMMANDS_GROUP_NAME, cols=cols)
append_plugins_cmd_to_cli(app, cli_group_name=COMMON_COMMANDS_GROUP_NAME, cols=cols)


# ==============
# ENTRY POINT
# To run from source:
#   - poetry run provisioner ...
# ==============
def main():
    app()
