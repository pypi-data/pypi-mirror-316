######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13                                                                                   #
# Generated on 2024-12-20T07:38:30.102332                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

