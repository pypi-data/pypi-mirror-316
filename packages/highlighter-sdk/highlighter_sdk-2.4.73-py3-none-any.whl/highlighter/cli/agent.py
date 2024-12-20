import hashlib
import json
import sys
from queue import Queue
from typing import Generator, Optional
from uuid import UUID, uuid4

import click

from highlighter.agent.agent import HLAgent, set_mock_aiko_messager
from highlighter.agent.capabilities.base_capability import DataSourceType
from highlighter.client.base_models.data_file import DataFile
from highlighter.client.gql_client import HLClient
from highlighter.client.tasks import (
    TaskStatus,
    lease_task,
    lease_tasks_from_steps,
    update_task_status,
)
from highlighter.core.logging import ColourStr


def _is_uuid(s):
    try:
        _ = UUID(s)
        return True
    except Exception as _:
        return False


def _compute_hash(b: bytes) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(b)
    return sha256_hash.hexdigest()


def iter_buffer(
    buffer,
    sep: Optional[int] = None,
    hash_queue: Optional[Queue] = None,
) -> Generator[bytes, None, None]:
    """
    Streams data from stdin until the Nth occurrence of a separator byte.

    sep: The separator byte value (e.g., b'\n' or b'\x00')
    hash_queue: A queue to put the hash of each byte chunk onto

    """
    byte_result = bytearray()

    # Reading from sys.stdin in binary mode
    while True:
        # Read one byte at a time from stdin
        # chunk = buffer.read(1024)
        chunk = buffer.read(8)
        if not chunk:
            if len(byte_result):
                byte_result = bytes(byte_result)
                if hash_queue is not None:
                    hash_queue.put(_compute_hash(byte_result))
                yield byte_result
            break

        for byte in chunk:
            if not byte:  # End of stream or input
                break

            # Check for separator
            if byte == sep:
                byte_result = bytes(byte_result)
                if hash_queue is not None:
                    hash_queue.put(_compute_hash(byte_result))
                yield byte_result
                byte_result = bytearray()
            else:
                # Add byte to byte_result
                byte_result.append(byte)  # byte is a one-length bytes object


@click.group("agent")
@click.pass_context
def agent_group(ctx):
    pass


# ToDo: Now that I am not accepting cli passed stream params. Is this needed,
# or is it just handled by the aiko pipeline
def parse_stream_params(agent, agent_definition) -> dict:

    stream_params = {}
    for node in agent.pipeline_graph.nodes():
        node_name = node.name

        # Start with in code params
        default_stream_parameters = node.element.default_stream_parameters()

        # Overwite with global pipeline definition params
        global_pipeline_definition_params = {
            k: v
            for k, v in agent_definition.parameters
            if k in node.element.DefaultStreamParameters.model_fields
        }
        default_stream_parameters.update(global_pipeline_definition_params)

        # Overwite with per element pipeline definition paras
        element_definition = [e for e in agent_definition.elements if e.name == node_name][0]
        pipeline_element_definition_params = {
            k.replace(f"{node_name}.", ""): v
            for k, v in element_definition.parameters.items()
            if k.replace(f"{node_name}.", "") in node.element.DefaultStreamParameters.model_fields
        }
        node.element.parameters = pipeline_element_definition_params
        default_stream_parameters.update(pipeline_element_definition_params)

        ele_stream_params = node.element.DefaultStreamParameters(**default_stream_parameters).model_dump()

        stream_params.update({f"{element_definition.name}.{k}": v for k, v in ele_stream_params.items()})

    return stream_params


def iter_queue(q):
    while not q.empty():
        return q.get()


class OnAgentError:
    def __init__(self, task_id=None):
        self.task_id = task_id

    def __call__(self, agent):
        print(ColourStr.red(f"Task {self.task_id} FAILED: {agent.hl_task_status_info}"))
        if self.task_id is not None:
            client = HLClient.get_client()
            update_task_status(
                client,
                str(self.task_id),
                TaskStatus.FAILED,
                message=json.dumps(agent.hl_task_status_info["message"]),
            )


class OnAgentStop:
    def __init__(self, task_id=None):
        self.task_id = task_id

    def __call__(self, agent):
        print(ColourStr.green(f"Task {self.task_id} SUCCESS: {agent.hl_task_status_info}"))
        if self.task_id is not None:
            client = HLClient.get_client()
            update_task_status(
                client,
                str(self.task_id),
                TaskStatus.SUCCESS,
                message=json.dumps(agent.hl_task_status_info["message"]),
            )


def _get_next_task_data_sources_from_step_id(step_id, client):
    step_id = UUID(step_id)

    def get_next():
        while True:
            tasks = lease_tasks_from_steps(
                client,
                [step_id],
                lease_sec=3600,
                filter_by_status="PENDING",
                set_status_to="RUNNING",
                count=1,
            )
            if not tasks:
                return None

            task = tasks[0]
            file_urls = [d.file_url_original for d in task.case.latest_submission.data_files]
            file_ids = [d.uuid for d in task.case.latest_submission.data_files]
            media_types = [d.content_type for d in task.case.latest_submission.data_files]

            data_sources = [
                DataSourceType(media_type=m, url=u, id=i) for m, u, i in zip(media_types, file_urls, file_ids)
            ]
            yield task.id, data_sources

    return get_next()


def _get_next_task_data_sources_from_step_task_ids(step_task_ids, client):
    step_task_ids = step_task_ids.split(",")
    assert all([_is_uuid(i) for i in step_task_ids])

    def get_next():
        for task_id in step_task_ids:
            task = lease_task(
                client,
                task_id=task_id,
                lease_sec=3600,
                set_status_to="RUNNING",
            )
            file_urls = [d.file_url_original for d in task.case.latest_submission.data_files]
            file_ids = [d.uuid for d in task.case.latest_submission.data_files]
            media_types = [d.content_type for d in task.case.latest_submission.data_files]

            data_sources = [
                DataSourceType(media_type=m, url=u, id=i) for m, u, i in zip(media_types, file_urls, file_ids)
            ]
            yield task.id, data_sources
        return None

    return get_next()


def _get_next_task_data_sources_from_filepaths(input_data, seperator):
    if input_data == "--":
        file_paths = iter([f.decode("utf-8") for f in iter_buffer(sys.stdin.buffer, sep=seperator)])
    else:
        file_paths = input_data.split(seperator)

    def get_next():
        for i, filepath in enumerate(file_paths):
            data_source = DataSourceType(media_type="", url=filepath, id=UUID(int=i))
            yield None, [data_source]

    return get_next()


def _get_next_task_data_sources_from_stdin_raw_data(input_data, seperator):
    def get_next():
        for i, content in enumerate(iter_buffer(sys.stdin.buffer, sep=seperator)):
            data_source = DataSourceType(media_type="", url="bytes://", id=UUID(int=i), content=content)
            yield None, [data_source]

    return get_next()


def _reading_filepaths_from_stdin(input_data, expect_filepaths):
    return (input_data == "--") and (not sys.stdin.isatty() and (expect_filepaths))


def _reading_raw_data_from_stdin(input_data, expect_filepaths):
    return (input_data == "--") and (not sys.stdin.isatty() and (not expect_filepaths))


def _reading_filepaths_from_input_data(input_data, expect_filepaths):
    return isinstance(input_data, str) and (input_data != "--") and (expect_filepaths)


def loop_over_task_data_sources(agent, stream_id, input_name, get_next_task_iter):

    for i, (task_id, data_sources) in enumerate(get_next_task_iter):

        stream_parameters: dict = parse_stream_params(
            agent.pipeline,
            agent.pipeline_definition,
        )
        stream_parameters[input_name] = data_sources

        if task_id is not None:
            agent.set_callback("on_agent_error", OnAgentError(task_id=task_id))
            agent.set_callback("on_agent_stop", OnAgentStop(task_id=task_id))
            _stream_id = task_id
        else:
            _stream_id = UUID(fields=(stream_id, 0, 0, 0, 0, i))

        print(_stream_id)
        agent.run(
            _stream_id,
            stream_parameters,
            mqtt_connection_required=False,
        )
        agent.pipeline.destroy_stream(_stream_id)


def loop_over_process_frame(agent, stream_id, frame_datas):
    # This function can be removed once
    # the issue it's solving is resolved.
    # See to function's doc string for more info
    set_mock_aiko_messager()

    if isinstance(frame_datas, dict):
        frame_datas = [frame_datas]

    stream_parameters: dict = parse_stream_params(
        agent.pipeline,
        agent.pipeline_definition,
    )

    agent.pipeline.create_stream(stream_id, stream_parameters)
    for frame_id, frame in enumerate(frame_datas):
        stream = {
            "stream_id": stream_id,
            "frame_id": frame_id,
        }

        data_files = [
            DataFile(
                file_id=uuid4(),
                content=frame["content"],
                media_frame_index=0,
                content_type="text",
            )
        ]
        agent.pipeline.process_frame(stream, {"data_files": data_files})
    agent.pipeline.destroy_stream(stream_id)


DEFAULT_FILEPATH_SEPERATOR = "\n"
DEFAULT_CONTENT_SEPERATOR = "\x1c"


@agent_group.command("run")
@click.option(
    "--buffer-seperator",
    "-p",
    type=str,
    default=None,
    help="If --expect-filepaths is set the default is '\\n'. Else the the unix file seperator '\\x1c'. This parameter is only used for piped inputs, if passing paths directly use spaces to separate paths",
)
@click.option("--expect-filepaths", "-f", is_flag=True, default=False)
@click.option("--step-task-ids", "-t", type=str, default=None)
@click.option("--step-id", "-i", type=str, default=None)
@click.option("--stream-id", "-s", type=int, default=1)
@click.option("--dump-definition", type=str, default=None)
@click.option("--input-name", type=str, default="Source.data_sources")
@click.argument("agent_definition", type=click.Path(dir_okay=False, exists=False))
@click.argument("input_data", type=click.Path(exists=False), default="--", required=False)
@click.pass_context
def _run(
    ctx,
    buffer_seperator,
    expect_filepaths,
    step_task_ids,
    step_id,
    stream_id,
    dump_definition,
    input_name,
    agent_definition,
    input_data,
):
    """Run a local Highlighter Agent to process data either on your local machine or as Highlighter Tasks.

    When processing local files, a mock task is constructed containing a single
    data file (e.g., image, text, video). Each file results in one stream. For
    example, if you're processing a set of images, each image will create a new
    stream, with each stream processing a single frame. In the case of a video,
    a stream will be created for each video, and each stream will process every
    frame of its respective video.

    Similarly, when processing Highlighter tasks, a stream is created for each
    task, and each stream processes all the data within that task. For instance,
    if a task contains several images, all the images in that task will be
    processed within the corresponding stream.

    The Agent definition must have its first element as a
    `DataSourceCapability`, such as `ImageDataSource`, `VideoDataSource`,
    `TextDataSource`, `JsonArrayDataSource`, etc. The following examples assume
    the use of `ImageDataSource`.

    Examples:

      \b
      1. Run an agent against a single image path
      \b
        > hl agent run -f agent-def.json images/123.jpg

      \b
      2. Run an agent against a multiple image paths
      \b
        > find -name *.jpg images/ | hl agent run -f agent-def.json

      \b
      3. Cat the contents of an image to an agent
      \b
        > images/123.jpg | hl agent run -f agent-def.json

      \b
      4. Pass data directly to process_frame
      \b
        > hl agent run -f agent-def.json '[{"foo": "bar"},{"foo": "baz"}]'

    """
    if step_id and step_task_ids:
        raise ValueError()

    client = ctx.obj["client"]
    if step_id:

        get_next_task_iter = _get_next_task_data_sources_from_step_id(step_id, client)

    elif step_task_ids:

        get_next_task_iter = _get_next_task_data_sources_from_step_task_ids(step_task_ids, client)

    elif _reading_raw_data_from_stdin(input_data, expect_filepaths):

        if buffer_seperator is None:
            seperator = ord(DEFAULT_CONTENT_SEPERATOR)
        else:
            seperator = ord(bytes(buffer_seperator, "utf-8").decode("unicode_escape"))

        get_next_task_iter = _get_next_task_data_sources_from_stdin_raw_data(input_data, seperator)

    elif _reading_filepaths_from_stdin(input_data, expect_filepaths):

        if buffer_seperator is None:
            seperator = ord(DEFAULT_FILEPATH_SEPERATOR)
        else:
            seperator = ord(bytes(buffer_seperator, "utf-8").decode("unicode_escape"))
        get_next_task_iter = _get_next_task_data_sources_from_filepaths(input_data, seperator)

    elif _reading_filepaths_from_input_data(input_data, expect_filepaths):

        get_next_task_iter = _get_next_task_data_sources_from_filepaths(input_data, ",")

    else:
        # assume process_frame_data is passed in directly either as a json
        # str in input_data or via sdtin buffer
        # assert False, f"-------------: {input_data}"
        try:
            if input_data == "--":
                frame_datas = json.load(sys.stdin.buffer)
            else:
                frame_datas = json.loads(input_data)
        except Exception as e:
            raise ValueError(f"{e} -- {input_data}")

        get_next_task_iter = None

    agent = HLAgent(agent_definition, dump_definition=dump_definition)

    if get_next_task_iter is None:
        loop_over_process_frame(agent, stream_id, frame_datas)
    else:
        loop_over_task_data_sources(agent, stream_id, input_name, get_next_task_iter)

    # for task in tasks:
    #    assessment_uuid = task.case.latest_submission.uuid
    #    endpoint_url = HLClient.get_client().endpoint_url
    #    endpoint_url = endpoint_url.replace("graphql", f"oid/assessment/{assessment_uuid}")
    #    data_sources = {
    #        "HlAssessmentRead": {
    #            "media_type": "highlighter-assessment",
    #            "url": endpoint_url,
    #        }
    #    }

    #    _stream_parameters: dict = parse_stream_params(
    #        agent.pipeline,
    #        agent.pipeline_definition,
    #        stream_parameters,
    #        params={"data_sources": data_sources},
    #    )

    #    stream_id = task.id
    #    agent.run(
    #        stream_id,
    #        _stream_parameters,
    #        mqtt_connection_required=False,
    #    )
