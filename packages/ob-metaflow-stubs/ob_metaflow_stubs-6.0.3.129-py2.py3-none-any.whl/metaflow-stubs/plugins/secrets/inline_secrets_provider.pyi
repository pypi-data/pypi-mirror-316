######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.0.1+obcheckpoint(0.1.6);ob(v1)                                                    #
# Generated on 2024-12-20T17:11:09.703617                                                            #
######################################################################################################

from __future__ import annotations

import abc
import metaflow
import typing
if typing.TYPE_CHECKING:
    import abc
    import metaflow.plugins.secrets

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

