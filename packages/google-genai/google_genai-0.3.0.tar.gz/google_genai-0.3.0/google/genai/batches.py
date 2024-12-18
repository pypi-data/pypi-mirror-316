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

from typing import Optional, Union
from urllib.parse import urlencode
from . import _common
from . import _extra_utils
from . import _transformers as t
from . import types
from ._api_client import ApiClient
from ._common import get_value_by_path as getv
from ._common import set_value_by_path as setv
from .pagers import AsyncPager, Pager


def _BatchJobSource_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['format']):
    raise ValueError('format parameter is not supported in Google AI.')

  if getv(from_object, ['gcs_uri']):
    raise ValueError('gcs_uri parameter is not supported in Google AI.')

  if getv(from_object, ['bigquery_uri']):
    raise ValueError('bigquery_uri parameter is not supported in Google AI.')

  return to_object


def _BatchJobSource_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['format']) is not None:
    setv(to_object, ['instancesFormat'], getv(from_object, ['format']))

  if getv(from_object, ['gcs_uri']) is not None:
    setv(to_object, ['gcsSource', 'uris'], getv(from_object, ['gcs_uri']))

  if getv(from_object, ['bigquery_uri']) is not None:
    setv(
        to_object,
        ['bigquerySource', 'inputUri'],
        getv(from_object, ['bigquery_uri']),
    )

  return to_object


def _BatchJobDestination_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['format']):
    raise ValueError('format parameter is not supported in Google AI.')

  if getv(from_object, ['gcs_uri']):
    raise ValueError('gcs_uri parameter is not supported in Google AI.')

  if getv(from_object, ['bigquery_uri']):
    raise ValueError('bigquery_uri parameter is not supported in Google AI.')

  return to_object


def _BatchJobDestination_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['format']) is not None:
    setv(to_object, ['predictionsFormat'], getv(from_object, ['format']))

  if getv(from_object, ['gcs_uri']) is not None:
    setv(
        to_object,
        ['gcsDestination', 'outputUriPrefix'],
        getv(from_object, ['gcs_uri']),
    )

  if getv(from_object, ['bigquery_uri']) is not None:
    setv(
        to_object,
        ['bigqueryDestination', 'outputUri'],
        getv(from_object, ['bigquery_uri']),
    )

  return to_object


def _CreateBatchJobConfig_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['http_options']) is not None:
    setv(to_object, ['httpOptions'], getv(from_object, ['http_options']))

  if getv(from_object, ['display_name']) is not None:
    setv(parent_object, ['displayName'], getv(from_object, ['display_name']))

  if getv(from_object, ['dest']):
    raise ValueError('dest parameter is not supported in Google AI.')

  return to_object


def _CreateBatchJobConfig_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['http_options']) is not None:
    setv(to_object, ['httpOptions'], getv(from_object, ['http_options']))

  if getv(from_object, ['display_name']) is not None:
    setv(parent_object, ['displayName'], getv(from_object, ['display_name']))

  if getv(from_object, ['dest']) is not None:
    setv(
        parent_object,
        ['outputConfig'],
        _BatchJobDestination_to_vertex(
            api_client,
            t.t_batch_job_destination(api_client, getv(from_object, ['dest'])),
            to_object,
        ),
    )

  return to_object


def _CreateBatchJobParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['model']):
    raise ValueError('model parameter is not supported in Google AI.')

  if getv(from_object, ['src']):
    raise ValueError('src parameter is not supported in Google AI.')

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _CreateBatchJobConfig_to_mldev(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _CreateBatchJobParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['model']) is not None:
    setv(
        to_object,
        ['model'],
        t.t_model(api_client, getv(from_object, ['model'])),
    )

  if getv(from_object, ['src']) is not None:
    setv(
        to_object,
        ['inputConfig'],
        _BatchJobSource_to_vertex(
            api_client,
            t.t_batch_job_source(api_client, getv(from_object, ['src'])),
            to_object,
        ),
    )

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _CreateBatchJobConfig_to_vertex(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _GetBatchJobConfig_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['http_options']) is not None:
    setv(to_object, ['httpOptions'], getv(from_object, ['http_options']))

  return to_object


def _GetBatchJobConfig_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['http_options']) is not None:
    setv(to_object, ['httpOptions'], getv(from_object, ['http_options']))

  return to_object


def _GetBatchJobParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']):
    raise ValueError('name parameter is not supported in Google AI.')

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _GetBatchJobConfig_to_mldev(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _GetBatchJobParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(
        to_object,
        ['_url', 'name'],
        t.t_batch_job_name(api_client, getv(from_object, ['name'])),
    )

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _GetBatchJobConfig_to_vertex(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _CancelBatchJobConfig_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['http_options']) is not None:
    setv(to_object, ['httpOptions'], getv(from_object, ['http_options']))

  return to_object


def _CancelBatchJobConfig_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['http_options']) is not None:
    setv(to_object, ['httpOptions'], getv(from_object, ['http_options']))

  return to_object


def _CancelBatchJobParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']):
    raise ValueError('name parameter is not supported in Google AI.')

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _CancelBatchJobConfig_to_mldev(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _CancelBatchJobParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(
        to_object,
        ['_url', 'name'],
        t.t_batch_job_name(api_client, getv(from_object, ['name'])),
    )

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _CancelBatchJobConfig_to_vertex(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _ListBatchJobConfig_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['http_options']) is not None:
    setv(to_object, ['httpOptions'], getv(from_object, ['http_options']))

  if getv(from_object, ['page_size']) is not None:
    setv(
        parent_object, ['_query', 'pageSize'], getv(from_object, ['page_size'])
    )

  if getv(from_object, ['page_token']) is not None:
    setv(
        parent_object,
        ['_query', 'pageToken'],
        getv(from_object, ['page_token']),
    )

  if getv(from_object, ['filter']):
    raise ValueError('filter parameter is not supported in Google AI.')

  return to_object


def _ListBatchJobConfig_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['http_options']) is not None:
    setv(to_object, ['httpOptions'], getv(from_object, ['http_options']))

  if getv(from_object, ['page_size']) is not None:
    setv(
        parent_object, ['_query', 'pageSize'], getv(from_object, ['page_size'])
    )

  if getv(from_object, ['page_token']) is not None:
    setv(
        parent_object,
        ['_query', 'pageToken'],
        getv(from_object, ['page_token']),
    )

  if getv(from_object, ['filter']) is not None:
    setv(parent_object, ['_query', 'filter'], getv(from_object, ['filter']))

  return to_object


def _ListBatchJobParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['config']):
    raise ValueError('config parameter is not supported in Google AI.')

  return to_object


def _ListBatchJobParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _ListBatchJobConfig_to_vertex(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _DeleteBatchJobParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']):
    raise ValueError('name parameter is not supported in Google AI.')

  return to_object


def _DeleteBatchJobParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(
        to_object,
        ['_url', 'name'],
        t.t_batch_job_name(api_client, getv(from_object, ['name'])),
    )

  return to_object


def _JobError_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}

  return to_object


def _JobError_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['details']) is not None:
    setv(to_object, ['details'], getv(from_object, ['details']))

  if getv(from_object, ['code']) is not None:
    setv(to_object, ['code'], getv(from_object, ['code']))

  if getv(from_object, ['message']) is not None:
    setv(to_object, ['message'], getv(from_object, ['message']))

  return to_object


def _BatchJobSource_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}

  return to_object


def _BatchJobSource_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['instancesFormat']) is not None:
    setv(to_object, ['format'], getv(from_object, ['instancesFormat']))

  if getv(from_object, ['gcsSource', 'uris']) is not None:
    setv(to_object, ['gcs_uri'], getv(from_object, ['gcsSource', 'uris']))

  if getv(from_object, ['bigquerySource', 'inputUri']) is not None:
    setv(
        to_object,
        ['bigquery_uri'],
        getv(from_object, ['bigquerySource', 'inputUri']),
    )

  return to_object


def _BatchJobDestination_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}

  return to_object


def _BatchJobDestination_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['predictionsFormat']) is not None:
    setv(to_object, ['format'], getv(from_object, ['predictionsFormat']))

  if getv(from_object, ['gcsDestination', 'outputUriPrefix']) is not None:
    setv(
        to_object,
        ['gcs_uri'],
        getv(from_object, ['gcsDestination', 'outputUriPrefix']),
    )

  if getv(from_object, ['bigqueryDestination', 'outputUri']) is not None:
    setv(
        to_object,
        ['bigquery_uri'],
        getv(from_object, ['bigqueryDestination', 'outputUri']),
    )

  return to_object


def _BatchJob_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}

  return to_object


def _BatchJob_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(to_object, ['name'], getv(from_object, ['name']))

  if getv(from_object, ['displayName']) is not None:
    setv(to_object, ['display_name'], getv(from_object, ['displayName']))

  if getv(from_object, ['state']) is not None:
    setv(to_object, ['state'], getv(from_object, ['state']))

  if getv(from_object, ['error']) is not None:
    setv(
        to_object,
        ['error'],
        _JobError_from_vertex(
            api_client, getv(from_object, ['error']), to_object
        ),
    )

  if getv(from_object, ['createTime']) is not None:
    setv(to_object, ['create_time'], getv(from_object, ['createTime']))

  if getv(from_object, ['startTime']) is not None:
    setv(to_object, ['start_time'], getv(from_object, ['startTime']))

  if getv(from_object, ['endTime']) is not None:
    setv(to_object, ['end_time'], getv(from_object, ['endTime']))

  if getv(from_object, ['updateTime']) is not None:
    setv(to_object, ['update_time'], getv(from_object, ['updateTime']))

  if getv(from_object, ['model']) is not None:
    setv(to_object, ['model'], getv(from_object, ['model']))

  if getv(from_object, ['inputConfig']) is not None:
    setv(
        to_object,
        ['src'],
        _BatchJobSource_from_vertex(
            api_client, getv(from_object, ['inputConfig']), to_object
        ),
    )

  if getv(from_object, ['outputConfig']) is not None:
    setv(
        to_object,
        ['dest'],
        _BatchJobDestination_from_vertex(
            api_client, getv(from_object, ['outputConfig']), to_object
        ),
    )

  return to_object


def _ListBatchJobResponse_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['nextPageToken']) is not None:
    setv(to_object, ['next_page_token'], getv(from_object, ['nextPageToken']))

  return to_object


def _ListBatchJobResponse_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['nextPageToken']) is not None:
    setv(to_object, ['next_page_token'], getv(from_object, ['nextPageToken']))

  if getv(from_object, ['batchPredictionJobs']) is not None:
    setv(
        to_object,
        ['batch_jobs'],
        [
            _BatchJob_from_vertex(api_client, item, to_object)
            for item in getv(from_object, ['batchPredictionJobs'])
        ],
    )

  return to_object


def _DeleteResourceJob_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}

  return to_object


def _DeleteResourceJob_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(to_object, ['name'], getv(from_object, ['name']))

  if getv(from_object, ['done']) is not None:
    setv(to_object, ['done'], getv(from_object, ['done']))

  if getv(from_object, ['error']) is not None:
    setv(
        to_object,
        ['error'],
        _JobError_from_vertex(
            api_client, getv(from_object, ['error']), to_object
        ),
    )

  return to_object


class Batches(_common.BaseModule):

  def _create(
      self,
      *,
      model: str,
      src: str,
      config: Optional[types.CreateBatchJobConfigOrDict] = None,
  ) -> types.BatchJob:
    parameter_model = types._CreateBatchJobParameters(
        model=model,
        src=src,
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _CreateBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'post', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _BatchJob_from_vertex(self.api_client, response_dict)
    else:
      response_dict = _BatchJob_from_mldev(self.api_client, response_dict)

    return_value = types.BatchJob._from_response(response_dict, parameter_model)
    self.api_client._verify_response(return_value)
    return return_value

  def get(
      self, *, name: str, config: Optional[types.GetBatchJobConfigOrDict] = None
  ) -> types.BatchJob:
    """Gets a batch job.

    Args:
      name (str): A fully-qualified BatchJob resource name or ID.
        Example: "projects/.../locations/.../batchPredictionJobs/456" or "456"
          when project and location are initialized in the client.

    Returns:
      A BatchJob object that contains details about the batch job.

    Usage:

    .. code-block:: python

      batch_job = client.batches.get(name='123456789')
      print(f"Batch job: {batch_job.name}, state {batch_job.state}")
    """

    parameter_model = types._GetBatchJobParameters(
        name=name,
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _GetBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs/{name}'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'get', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _BatchJob_from_vertex(self.api_client, response_dict)
    else:
      response_dict = _BatchJob_from_mldev(self.api_client, response_dict)

    return_value = types.BatchJob._from_response(response_dict, parameter_model)
    self.api_client._verify_response(return_value)
    return return_value

  def cancel(
      self,
      *,
      name: str,
      config: Optional[types.CancelBatchJobConfigOrDict] = None,
  ) -> None:
    parameter_model = types._CancelBatchJobParameters(
        name=name,
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _CancelBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs/{name}:cancel'.format_map(
          request_dict.get('_url')
      )

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'post', path, request_dict, http_options
    )

  def _list(
      self, *, config: types.ListBatchJobConfigOrDict
  ) -> types.ListBatchJobResponse:
    parameter_model = types._ListBatchJobParameters(
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _ListBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'get', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _ListBatchJobResponse_from_vertex(
          self.api_client, response_dict
      )
    else:
      response_dict = _ListBatchJobResponse_from_mldev(
          self.api_client, response_dict
      )

    return_value = types.ListBatchJobResponse._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  def delete(self, *, name: str) -> types.DeleteResourceJob:
    """Deletes a batch job.

    Args:
      name (str): A fully-qualified BatchJob resource name or ID.
        Example: "projects/.../locations/.../batchPredictionJobs/456" or "456"
          when project and location are initialized in the client.

    Returns:
      A DeleteResourceJob object that shows the status of the deletion.

    Usage:

    .. code-block:: python

      client.batches.delete(name='123456789')
    """

    parameter_model = types._DeleteBatchJobParameters(
        name=name,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _DeleteBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs/{name}'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'delete', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _DeleteResourceJob_from_vertex(
          self.api_client, response_dict
      )
    else:
      response_dict = _DeleteResourceJob_from_mldev(
          self.api_client, response_dict
      )

    return_value = types.DeleteResourceJob._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  def create(
      self,
      *,
      model: str,
      src: str,
      config: Optional[types.CreateBatchJobConfigOrDict] = None,
  ) -> types.BatchJob:
    """Creates a batch job.

    Args:
      model (str): The model to use for the batch job.
      src (str): The source of the batch job. Currently supports GCS URI(-s) or
        Bigquery URI. Example: "gs://path/to/input/data" or
        "bq://projectId.bqDatasetId.bqTableId".
      config (CreateBatchJobConfig): Optional configuration for the batch job.

    Returns:
      A BatchJob object that contains details about the batch job.

    Usage:

    .. code-block:: python

      batch_job = client.batches.create(
          model="gemini-1.5-flash",
          src="gs://path/to/input/data",
      )
      print(batch_job.state)
    """
    config = _extra_utils.format_destination(src, config)
    return self._create(model=model, src=src, config=config)

  def list(
      self, *, config: Optional[types.ListBatchJobConfigOrDict] = None
  ) -> Pager[types.BatchJob]:
    """Lists batch jobs.

    Args:
      config (ListBatchJobConfig): Optional configuration for the list request.

    Returns:
      A Pager object that contains one page of batch jobs. When iterating over
      the pager, it automatically fetches the next page if there are more.

    Usage:

    .. code-block:: python

      batch_jobs = client.batches.list(config={"page_size": 10})
      for batch_job in batch_jobs:
        print(f"Batch job: {batch_job.name}, state {batch_job.state}")
    """
    return Pager(
        'batch_jobs',
        self._list,
        self._list(config=config),
        config,
    )


class AsyncBatches(_common.BaseModule):

  async def _create(
      self,
      *,
      model: str,
      src: str,
      config: Optional[types.CreateBatchJobConfigOrDict] = None,
  ) -> types.BatchJob:
    parameter_model = types._CreateBatchJobParameters(
        model=model,
        src=src,
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _CreateBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'post', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _BatchJob_from_vertex(self.api_client, response_dict)
    else:
      response_dict = _BatchJob_from_mldev(self.api_client, response_dict)

    return_value = types.BatchJob._from_response(response_dict, parameter_model)
    self.api_client._verify_response(return_value)
    return return_value

  async def get(
      self, *, name: str, config: Optional[types.GetBatchJobConfigOrDict] = None
  ) -> types.BatchJob:
    """Gets a batch job.

    Args:
      name (str): A fully-qualified BatchJob resource name or ID.
        Example: "projects/.../locations/.../batchPredictionJobs/456" or "456"
          when project and location are initialized in the client.

    Returns:
      A BatchJob object that contains details about the batch job.

    Usage:

    .. code-block:: python

      batch_job = client.batches.get(name='123456789')
      print(f"Batch job: {batch_job.name}, state {batch_job.state}")
    """

    parameter_model = types._GetBatchJobParameters(
        name=name,
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _GetBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs/{name}'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'get', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _BatchJob_from_vertex(self.api_client, response_dict)
    else:
      response_dict = _BatchJob_from_mldev(self.api_client, response_dict)

    return_value = types.BatchJob._from_response(response_dict, parameter_model)
    self.api_client._verify_response(return_value)
    return return_value

  async def cancel(
      self,
      *,
      name: str,
      config: Optional[types.CancelBatchJobConfigOrDict] = None,
  ) -> None:
    parameter_model = types._CancelBatchJobParameters(
        name=name,
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _CancelBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs/{name}:cancel'.format_map(
          request_dict.get('_url')
      )

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'post', path, request_dict, http_options
    )

  async def _list(
      self, *, config: types.ListBatchJobConfigOrDict
  ) -> types.ListBatchJobResponse:
    parameter_model = types._ListBatchJobParameters(
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _ListBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'get', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _ListBatchJobResponse_from_vertex(
          self.api_client, response_dict
      )
    else:
      response_dict = _ListBatchJobResponse_from_mldev(
          self.api_client, response_dict
      )

    return_value = types.ListBatchJobResponse._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  async def delete(self, *, name: str) -> types.DeleteResourceJob:
    """Deletes a batch job.

    Args:
      name (str): A fully-qualified BatchJob resource name or ID.
        Example: "projects/.../locations/.../batchPredictionJobs/456" or "456"
          when project and location are initialized in the client.

    Returns:
      A DeleteResourceJob object that shows the status of the deletion.

    Usage:

    .. code-block:: python

      client.batches.delete(name='123456789')
    """

    parameter_model = types._DeleteBatchJobParameters(
        name=name,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _DeleteBatchJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'batchPredictionJobs/{name}'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'delete', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _DeleteResourceJob_from_vertex(
          self.api_client, response_dict
      )
    else:
      response_dict = _DeleteResourceJob_from_mldev(
          self.api_client, response_dict
      )

    return_value = types.DeleteResourceJob._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  async def create(
      self,
      *,
      model: str,
      src: str,
      config: Optional[types.CreateBatchJobConfigOrDict] = None,
  ) -> types.BatchJob:
    """Creates a batch job asynchronously.

    Args:
      model (str): The model to use for the batch job.
      src (str): The source of the batch job. Currently supports GCS URI(-s) or
        Bigquery URI. Example: "gs://path/to/input/data" or
        "bq://projectId.bqDatasetId.bqTableId".
      config (CreateBatchJobConfig): Optional configuration for the batch job.

    Returns:
      A BatchJob object that contains details about the batch job.

    Usage:

    .. code-block:: python

      batch_job = await client.aio.batches.create(
          model="gemini-1.5-flash",
          src="gs://path/to/input/data",
      )
    """
    config = _extra_utils.format_destination(src, config)
    return await self._create(model=model, src=src, config=config)

  async def list(
      self, *, config: Optional[types.ListBatchJobConfigOrDict] = None
  ) -> AsyncPager[types.BatchJob]:
    """Lists batch jobs asynchronously.

    Args:
      config (ListBatchJobConfig): Optional configuration for the list request.

    Returns:
      A Pager object that contains one page of batch jobs. When iterating over
      the pager, it automatically fetches the next page if there are more.

    Usage:

    .. code-block:: python

      batch_jobs = await client.aio.batches.list(config={'page_size': 5})
      print(f"current page: {batch_jobs.page}")
      await batch_jobs_pager.next_page()
      print(f"next page: {batch_jobs_pager.page}")
    """
    return AsyncPager(
        'batch_jobs',
        self._list,
        await self._list(config=config),
        config,
    )
