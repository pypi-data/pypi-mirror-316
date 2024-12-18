######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.39.1+obcheckpoint(0.1.6);ob(v1)                                                   #
# Generated on 2024-12-18T07:29:34.059298                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

