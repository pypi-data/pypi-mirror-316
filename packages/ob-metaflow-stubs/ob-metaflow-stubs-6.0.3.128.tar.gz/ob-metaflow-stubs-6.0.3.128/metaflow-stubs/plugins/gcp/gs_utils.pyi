######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.39.1+obcheckpoint(0.1.6);ob(v1)                                                   #
# Generated on 2024-12-18T07:29:34.057287                                                            #
######################################################################################################

from __future__ import annotations


from ...exception import MetaflowException as MetaflowException
from ...exception import MetaflowInternalError as MetaflowInternalError
from .gs_exceptions import MetaflowGSPackageError as MetaflowGSPackageError

def parse_gs_full_path(gs_uri):
    ...

def check_gs_deps(func):
    """
    The decorated function checks GS dependencies (as needed for Google Cloud storage backend). This includes
    various GCP SDK packages, as well as a Python version of >=3.7
    """
    ...

def process_gs_exception(*args, **kwargs):
    ...

