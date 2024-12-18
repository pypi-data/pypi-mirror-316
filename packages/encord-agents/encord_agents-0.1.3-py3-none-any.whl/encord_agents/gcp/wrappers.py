import logging
from contextlib import ExitStack
from functools import wraps
from typing import Any, Callable

import orjson
from encord.objects.ontology_labels_impl import LabelRowV2
from flask import Request, Response, make_response

from encord_agents import FrameData
from encord_agents.core.data_model import LabelRowInitialiseLabelsArgs, LabelRowMetadataIncludeArgs
from encord_agents.core.dependencies.models import Context
from encord_agents.core.dependencies.utils import get_dependant, solve_dependencies
from encord_agents.core.utils import get_user_client

AgentFunction = Callable[..., Any]


def generate_response() -> Response:
    """
    Generate a Response object with status 200 in order to tell the FE that the function has finished successfully.
    :return: Response object with the right CORS settings.
    """
    response = make_response("")
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def editor_agent(
    *,
    label_row_metadata_include_args: LabelRowMetadataIncludeArgs | None = None,
    label_row_initialise_labels_args: LabelRowInitialiseLabelsArgs | None = None,
) -> Callable[[AgentFunction], Callable[[Request], Response]]:
    """
    Wrapper to make resources available for gcp editor agents.

    The editor agents are intended to be used via dependency injections.
    You can learn more via out [documentation](https://agents-docs.encord.com).

    Args:
        label_row_metadata_include_args: arguments to overwrite default arguments
            on `project.list_label_rows_v2()`.
        label_row_initialise_labels_args: Arguments to overwrite default arguments
            on `label_row.initialise_labels(...)`

    Returns:
        A wrapped function suitable for gcp functions.
    """

    def context_wrapper_inner(func: AgentFunction) -> Callable[[Request], Response]:
        dependant = get_dependant(func=func)

        @wraps(func)
        def wrapper(request: Request) -> Response:
            frame_data = FrameData.model_validate_json(orjson.dumps(request.form.to_dict()))
            logging.info(f"Request: {frame_data}")

            client = get_user_client()
            project = client.get_project(str(frame_data.project_hash))

            label_row: LabelRowV2 | None = None
            if dependant.needs_label_row:
                include_args = label_row_metadata_include_args or LabelRowMetadataIncludeArgs()
                init_args = label_row_initialise_labels_args or LabelRowInitialiseLabelsArgs()
                label_row = project.list_label_rows_v2(
                    data_hashes=[str(frame_data.data_hash)], **include_args.model_dump()
                )[0]
                label_row.initialise_labels(**init_args.model_dump())

            context = Context(project=project, label_row=label_row, frame_data=frame_data)
            with ExitStack() as stack:
                dependencies = solve_dependencies(context=context, dependant=dependant, stack=stack)
                func(**dependencies.values)
            return generate_response()

        return wrapper

    return context_wrapper_inner
