######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.39.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-17T21:56:50.964919                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators
    import metaflow.flowspec
    import metaflow.graph

from ...metaflow_current import current as current
from ...events import Trigger as Trigger
from ...metadata_provider.metadata import MetaDatum as MetaDatum
from ...flowspec import FlowSpec as FlowSpec
from .argo_events import ArgoEvent as ArgoEvent

ARGO_EVENTS_WEBHOOK_URL: None

class ArgoWorkflowsInternalDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_finished(self, step_name, flow: metaflow.flowspec.FlowSpec, graph: metaflow.graph.FlowGraph, is_task_ok, retry_count, max_user_code_retries):
        ...
    ...

