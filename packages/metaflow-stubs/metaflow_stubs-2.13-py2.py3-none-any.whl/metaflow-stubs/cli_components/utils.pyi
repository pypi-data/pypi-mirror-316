######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13                                                                                   #
# Generated on 2024-12-20T07:38:30.096971                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow._vendor.click.core

from .._vendor import click as click

class LazyPluginCommandCollection(metaflow._vendor.click.core.CommandCollection, metaclass=type):
    def __init__(self, *args, lazy_sources = None, **kwargs):
        ...
    def invoke(self, ctx):
        ...
    def list_commands(self, ctx):
        ...
    def get_command(self, ctx, cmd_name):
        ...
    ...

class LazyGroup(metaflow._vendor.click.core.Group, metaclass=type):
    def __init__(self, *args, lazy_subcommands = None, **kwargs):
        ...
    def list_commands(self, ctx):
        ...
    def get_command(self, ctx, cmd_name):
        ...
    ...

