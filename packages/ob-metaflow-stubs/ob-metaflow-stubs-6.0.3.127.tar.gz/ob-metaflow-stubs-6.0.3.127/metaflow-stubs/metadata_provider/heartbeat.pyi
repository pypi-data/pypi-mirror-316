######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.39.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-17T21:56:50.934178                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ..exception import MetaflowException as MetaflowException

SERVICE_HEADERS: dict

HB_URL_KEY: str

class HeartBeatException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class MetadataHeartBeat(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    @classmethod
    def get_worker(cls):
        ...
    ...

