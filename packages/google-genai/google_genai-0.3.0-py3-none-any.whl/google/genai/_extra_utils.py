# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Extra utils depending on types that are shared between sync and async modules.
"""

import inspect
import logging
from typing import Any, Callable, Dict, get_args, get_origin, Optional, types as typing_types, Union

import pydantic

from . import _common
from . import errors
from . import types


_DEFAULT_MAX_REMOTE_CALLS_AFC = 10


def format_destination(
    src: str,
    config: Optional[types.CreateBatchJobConfigOrDict] = None,
) -> types.CreateBatchJobConfig:
  """Formats the destination uri based on the source uri."""
  config = (
      types._CreateBatchJobParameters(config=config).config
      or types.CreateBatchJobConfig()
  )

  unique_name = None
  if not config.display_name:
    unique_name = _common.timestamped_unique_name()
    config.display_name = f'genai_batch_job_{unique_name}'

  if not config.dest:
    if src.startswith('gs://') and src.endswith('.jsonl'):
      # If source uri is "gs://bucket/path/to/src.jsonl", then the destination
      # uri prefix will be "gs://bucket/path/to/src/dest".
      config.dest = f'{src[:-6]}/dest'
    elif src.startswith('bq://'):
      # If source uri is "bq://project.dataset.src", then the destination
      # uri will be "bq://project.dataset.src_dest_TIMESTAMP_UUID".
      unique_name = unique_name or _common.timestamped_unique_name()
      config.dest = f'{src}_dest_{unique_name}'
    else:
      raise ValueError(f'Unsupported source: {src}')
  return config


def get_function_map(
    config: Optional[types.GenerateContentConfigOrDict] = None,
) -> dict[str, object]:
  """Returns a function map from the config."""
  config_model = (
      types.GenerateContentConfig(**config)
      if config and isinstance(config, dict)
      else config
  )
  function_map = {}
  if not config_model:
    return function_map
  if config_model.tools:
    for tool in config_model.tools:
      if callable(tool):
        if inspect.iscoroutinefunction(tool):
          raise errors.UnsupportedFunctionError(
              f'Function {tool.__name__} is a coroutine function, which is not'
              ' supported for automatic function calling. Please manually invoke'
              f' {tool.__name__} to get the function response.'
          )
        function_map[tool.__name__] = tool
  return function_map


def convert_number_values_for_function_call_args(
    args: Union[dict[str, object], list[object], object],
) -> Union[dict[str, object], list[object], object]:
  """Converts float values with no decimal to integers."""
  if isinstance(args, float) and args.is_integer():
    return int(args)
  if isinstance(args, dict):
    return {
        key: convert_number_values_for_function_call_args(value)
        for key, value in args.items()
    }
  if isinstance(args, list):
    return [
        convert_number_values_for_function_call_args(value) for value in args
    ]
  return args


def _is_annotation_pydantic_model(annotation: Any) -> bool:
  return inspect.isclass(annotation) and issubclass(
      annotation, pydantic.BaseModel
  )


def convert_if_exist_pydantic_model(
    value: Any, annotation: Any, param_name: str, func_name: str
) -> Any:
  if isinstance(value, dict) and _is_annotation_pydantic_model(annotation):
    try:
      return annotation(**value)
    except pydantic.ValidationError as e:
      raise errors.UnkownFunctionCallArgumentError(
          f'Failed to parse parameter {param_name} for function'
          f' {func_name} from function call part because function call argument'
          f' value {value} is not compatible with parameter annotation'
          f' {annotation}, due to error {e}'
      )
  if isinstance(value, list) and get_origin(annotation) == list:
    item_type = get_args(annotation)[0]
    return [
        convert_if_exist_pydantic_model(item, item_type, param_name, func_name)
        for item in value
    ]
  if isinstance(value, dict) and get_origin(annotation) == dict:
    _, value_type = get_args(annotation)
    return {
        k: convert_if_exist_pydantic_model(v, value_type, param_name, func_name)
        for k, v in value.items()
    }
  # example 1: typing.Union[int, float]
  # example 2: int | float equivalent to typing.types.UnionType[int, float]
  if get_origin(annotation) in (Union, typing_types.UnionType):
    for arg in get_args(annotation):
      if isinstance(value, arg) or (
          isinstance(value, dict) and _is_annotation_pydantic_model(arg)
      ):
        try:
          return convert_if_exist_pydantic_model(
              value, arg, param_name, func_name
          )
        # do not raise here because there could be multiple pydantic model types
        # in the union type.
        except pydantic.ValidationError:
          continue
    # if none of the union type is matched, raise error
    raise errors.UnkownFunctionCallArgumentError(
        f'Failed to parse parameter {param_name} for function'
        f' {func_name} from function call part because function call argument'
        f' value {value} cannot be converted to parameter annotation'
        f' {annotation}.'
    )
  # the only exception for value and annotation type to be different is int and
  # float. see convert_number_values_for_function_call_args function for context
  if isinstance(value, int) and annotation is float:
    return value
  if not isinstance(value, annotation):
    raise errors.UnkownFunctionCallArgumentError(
        f'Failed to parse parameter {param_name} for function {func_name} from'
        f' function call part because function call argument value {value} is'
        f' not compatible with parameter annotation {annotation}.'
    )
  return value


def invoke_function_from_dict_args(
    args: Dict[str, Any], function_to_invoke: Callable
) -> Any:
  signature = inspect.signature(function_to_invoke)
  func_name = function_to_invoke.__name__
  converted_args = {}
  for param_name, param in signature.parameters.items():
    if param_name in args:
      converted_args[param_name] = convert_if_exist_pydantic_model(
          args[param_name],
          param.annotation,
          param_name,
          func_name,
      )
  try:
    return function_to_invoke(**converted_args)
  except Exception as e:
    raise errors.FunctionInvocationError(
        f'Failed to invoke function {func_name} with converted arguments'
        f' {converted_args} from model returned function call argument'
        f' {args} because of error {e}'
    )


def get_function_response_parts(
    response: types.GenerateContentResponse,
    function_map: dict[str, object],
) -> list[types.Part]:
  """Returns the function response parts from the response."""
  func_response_parts = []
  for part in response.candidates[0].content.parts:
    if not part.function_call:
      continue
    func_name = part.function_call.name
    func = function_map[func_name]
    args = convert_number_values_for_function_call_args(part.function_call.args)
    try:
      response = {'result': invoke_function_from_dict_args(args, func)}
    except Exception as e:  # pylint: disable=broad-except
      response = {'error': str(e)}
    func_response = types.Part.from_function_response(func_name, response)

    func_response_parts.append(func_response)
  return func_response_parts


def should_disable_afc(
    config: Optional[types.GenerateContentConfigOrDict] = None,
) -> bool:
  """Returns whether automatic function calling is enabled."""
  config_model = (
      types.GenerateContentConfig(**config)
      if config and isinstance(config, dict)
      else config
  )

  # If max_remote_calls is less or equal to 0, warn and disable AFC.
  if (
      config_model
      and config_model.automatic_function_calling
      and config_model.automatic_function_calling.maximum_remote_calls
      is not None
      and int(config_model.automatic_function_calling.maximum_remote_calls)
      <= 0
  ):
    logging.warning(
        'max_remote_calls in automatic_function_calling_config'
        f' {config_model.automatic_function_calling.maximum_remote_calls} is'
        ' less than or equal to 0. Disabling automatic function calling.'
        ' Please set max_remote_calls to a positive integer.'
    )
    return True

  # Default to enable AFC if not specified.
  if (
      not config_model
      or not config_model.automatic_function_calling
      or config_model.automatic_function_calling.disable is None
  ):
    return False

  if (
      config_model.automatic_function_calling.disable
      and config_model.automatic_function_calling.maximum_remote_calls
      is not None
      and int(config_model.automatic_function_calling.maximum_remote_calls) > 0
  ):
    logging.warning(
        '`automatic_function_calling.disable` is set to `True`. But'
        ' `automatic_function_calling.maximum_remote_calls` is set to be a'
        ' positive number'
        f' {config_model.automatic_function_calling.maximum_remote_calls}.'
        ' Disabling automatic function calling. If you want to enable'
        ' automatic function calling, please set'
        ' `automatic_function_calling.disable` to `False` or leave it unset,'
        ' and set `automatic_function_calling.maximum_remote_calls` to a'
        ' positive integer or leave'
        ' `automatic_function_calling.maximum_remote_calls` unset.'
    )

  return config_model.automatic_function_calling.disable


def get_max_remote_calls_afc(
    config: Optional[types.GenerateContentConfigOrDict] = None,
) -> int:
  """Returns the remaining remote calls for automatic function calling."""
  if should_disable_afc(config):
    raise ValueError(
        'automatic function calling is not enabled, but SDK is trying to get'
        ' max remote calls.'
    )
  config_model = (
      types.GenerateContentConfig(**config)
      if config and isinstance(config, dict)
      else config
  )
  if (
      not config_model
      or not config_model.automatic_function_calling
      or config_model.automatic_function_calling.maximum_remote_calls is None
  ):
    return _DEFAULT_MAX_REMOTE_CALLS_AFC
  return int(config_model.automatic_function_calling.maximum_remote_calls)

def should_append_afc_history(
    config: Optional[types.GenerateContentConfigOrDict] = None,
) -> bool:
  config_model = (
      types.GenerateContentConfig(**config)
      if config and isinstance(config, dict)
      else config
  )
  if (
      not config_model
      or not config_model.automatic_function_calling
  ):
    return True
  return not config_model.automatic_function_calling.ignore_call_history
