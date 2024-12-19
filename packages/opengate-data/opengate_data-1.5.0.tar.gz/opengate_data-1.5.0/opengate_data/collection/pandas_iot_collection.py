from datetime import datetime
from typing import Any
import pandas as pd
import json
from flatten_dict import unflatten

from opengate_data.utils.utils import send_request, handle_exception, set_method_call, \
    validate_type


class PandasIotCollectionBuilder:
    """Pandas Iot Collection Builder"""

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.headers = self.client.headers
        self.method_calls: list = []
        self.dataframe: pd.DataFrame | None = None
        self.columns: list = []
        self.max_request_size_bytes: int = 22020096
        self.payload: dict = {"devices": {}}


    @set_method_call
    def from_dataframe(self, df: pd.DataFrame) -> "PandasIotCollectionBuilder":
        validate_type(df, pd.DataFrame, "Dataframe")
        self.dataframe = df

        if 'device_id' not in self.dataframe.columns or 'at' not in self.dataframe.columns:
            raise Exception(
                "The dataframe does not contain the columns 'device_id' or 'at'. If no 'at' is provided, create the column with empty values"
            )

        self._process_dataframe(self.dataframe)
        return self

    @set_method_call
    def with_columns(self, columns: list[str]) -> "PandasIotCollectionBuilder":
        validate_type(columns, list, "Columns")
        for column in columns:
            validate_type(column, str, "Column name")
        self.columns = columns

        if self.dataframe is not None:
            for col in columns:
                if col not in self.dataframe.columns:
                    raise Exception(f"The column '{col}' does not exist. Please check the dataframe column names")
        else:
            raise Exception("Dataframe has not been set. Please call from_dataframe() before with_columns().")

        return self

    @set_method_call
    def with_max_bytes_per_request(self, max_bytes:int) -> "PandasIotCollectionBuilder":
        """
        Specifies the maximum number of bytes per request for IoT collection.
        """
        validate_type(max_bytes, int, "MaxBytes")
        self.max_request_size_bytes = max_bytes
        return self

    @set_method_call
    def build(self) -> "PandasIotCollectionBuilder":
        self._validate_builds()
        if 'build_execute' in self.method_calls:
            raise Exception("You cannot use build() together with build_execute()")

        return self

    @set_method_call
    def build_execute(self, include_payload=False):
        if 'build' in self.method_calls:
            raise ValueError("You cannot use build_execute() together with build()")

        if 'execute' in self.method_calls:
            raise ValueError("You cannot use build_execute() together with execute()")

        self._validate_builds()
        self._execute_pandas_collection(include_payload)

        return self._execute_pandas_collection(include_payload)

    @set_method_call
    def execute(self, include_payload=False):
        if 'build' in self.method_calls:
            if self.method_calls[-2] != 'build':
                raise Exception("The build() function must be the last method invoked before execute.")

        if 'build' not in self.method_calls and 'build_execute' not in self.method_calls:
            raise Exception(
                "You need to use a build() or build_execute() function as the last method invoked before execute."
            )

        collection_results = self._execute_pandas_collection(include_payload)

        result_dataframe = self.dataframe.copy()
        status_column = []
        at_column = []

        for _, row in result_dataframe.iterrows():
            device_id = row['device_id']
            at = None
            if device_id in self.payload['devices']:
                for datastream in self.payload['devices'][device_id]['datastreams']:
                    if datastream['datapoints']:
                        at = datastream['datapoints'][0].get('at', None)
                        if at is not None:
                            break

            if at is None:
                at = int(datetime.now().timestamp() * 1000)

            at_column.append(at)

            if device_id in collection_results:
                device_responses = collection_results[device_id]
                success_datastreams = []
                failed_datastreams = []
                failure_reasons = []

                for response in device_responses:
                    datastream_id = response.get('datastream_id', 'Unknown')
                    status = response.get('status', None)
                    error = response.get('error', None)

                    if status == "Success":
                        success_datastreams.append(datastream_id)
                    elif status == "Failed":
                        failed_datastreams.append(datastream_id)
                        if error:
                            failure_reasons.append(f"{datastream_id}: {error}")

                if not failed_datastreams:
                    status_column.append("Success")
                elif not success_datastreams:
                    status_column.append(
                        f"Failed: {', '.join(failed_datastreams)} - Reasons: {', '.join(failure_reasons)}"
                    )
                else:
                    status_column.append(
                        f"Partial Success - Failed: {', '.join(failed_datastreams)} - Reasons: {', '.join(failure_reasons)} "
                        f"- Success : {', '.join(success_datastreams)}"
                    )
            else:
                status_column.append(f"Failed (Unexpected Error for device {device_id})")

        result_dataframe['at'] = at_column
        result_dataframe['status'] = status_column

        return result_dataframe

    def _validate_builds(self):
        """
        Validates the configuration of the builder to ensure the methods are called in the correct order.
        """
        if 'from_dataframe' not in self.method_calls:
            raise Exception("Dataframe has not been set. Please call from_dataframe() before with_columns().")

        if 'with_columns' in self.method_calls:
            index_from_dataframe = self.method_calls.index('from_dataframe')
            index_with_columns = self.method_calls.index('with_columns')
            if index_with_columns < index_from_dataframe:
                raise Exception("from_dataframe() must be called before with_columns().")

        if self.dataframe is None:
            raise Exception("Dataframe has not been set. Please call from_dataframe() before build().")

        for col in self.columns:
            if col not in self.dataframe.columns:
                raise Exception(f"The column '{col}' does not exist. Please check the dataframe column names.")

        if 'build' in self.method_calls and 'build_execute' in self.method_calls:
            raise Exception("You cannot use build() together with build_execute().")

        if 'build_execute' not in self.method_calls and 'build' not in self.method_calls:
            raise Exception(
                "You need to use a build() or build_execute() function as the last method invoked before execute."
            )
    def _process_dataframe(self, df: pd.DataFrame):
        """
        Processes the dataframe, handling both dot and underscore keys.
        Ensures that 'current' markers are handled correctly without duplicating 'value'.
        """
        required_columns = ['device_id', 'at']
        optional_columns = ['origin_device_identifier', 'version', 'path', 'trustedboot', 'from']

        if not set(required_columns).issubset(df.columns):
            missing_cols = set(required_columns) - set(df.columns)
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        datastream_columns = [
            col for col in df.columns if col not in required_columns + optional_columns
        ]

        now_milliseconds = int(datetime.now().timestamp() * 1000)

        for index, row in df.iterrows():
            device_id = row['device_id']
            at = row.get('at', now_milliseconds)

            if isinstance(at, str):
                at = int(pd.to_datetime(at).timestamp() * 1000)

            if device_id not in self.payload['devices']:
                self.payload['devices'][device_id] = {"datastreams": [], "version": "1.0.0"}

            for col in datastream_columns:
                value = row.get(col, None)

                if value is None or (isinstance(value, (float, int)) and pd.isna(value)):
                    continue

                datastream_id = col.replace("_", ".")

                if 'current' in datastream_id:
                    parts = datastream_id.split('.')
                    current_index = parts.index('current')
                    datastream_id = '.'.join(parts[:current_index])
                    nested_key = '.'.join(parts[current_index + 1:])

                    nested_value = unflatten({nested_key: value}, splitter='dot')

                    while isinstance(nested_value, dict) and "value" in nested_value:
                        nested_value = nested_value["value"]

                    datapoint_value = nested_value
                else:
                    datapoint_value = value

                datapoint = {"value": datapoint_value, "at": at}
                self._add_datapoint_to_payload(device_id, datastream_id, datapoint)

        return self

    def _execute_pandas_collection(self, include_payload):
        results = {}
        errors = {}

        for device_id, device_data in self.payload.get('devices', {}).items():
            try:
                if self.client.url is None:
                    base_url = 'https://connector-tcp:9443'
                else:
                    base_url = f'{self.client.url}/south'
                url = f'{base_url}/v80/devices/{device_id}/collect/iot'

                batched_data = []
                current_batch = {"datastreams": [], "version": device_data["version"]}

                for datastream in device_data["datastreams"]:
                    partial_datastream = {"id": datastream["id"], "datapoints": []}
                    for datapoint in datastream["datapoints"]:
                        temp_datastream = {"id": datastream["id"], "datapoints": [datapoint]}
                        temp_batch = {
                            "datastreams": current_batch["datastreams"] + [temp_datastream],
                            "version": current_batch["version"]
                        }
                        temp_size = len(json.dumps(temp_batch).encode('utf-8'))

                        if temp_size > self.max_request_size_bytes:
                            single_datapoint_size = len(json.dumps({"datastreams": [temp_datastream]}).encode('utf-8'))
                            if single_datapoint_size >= self.max_request_size_bytes:
                                if device_id not in results:
                                    results[device_id] = []
                                results[device_id].append({
                                    "datastream_id": datastream["id"],
                                    "status": "Failed",
                                    "error": f"Request exceeded size limit ({self.max_request_size_bytes} bytes)"
                                })
                                continue

                            if current_batch["datastreams"]:
                                batched_data.append(current_batch)
                                current_batch = {"datastreams": [], "version": device_data["version"]}

                            current_batch["datastreams"].append(temp_datastream)
                        else:
                            partial_datastream["datapoints"].append(datapoint)

                    if partial_datastream["datapoints"]:
                        current_batch["datastreams"].append(partial_datastream)

                if current_batch["datastreams"]:
                    batched_data.append(current_batch)

                for batch in batched_data:
                    request_size = len(json.dumps(batch).encode('utf-8'))
                    if request_size > self.max_request_size_bytes:
                        if device_id not in results:
                            results[device_id] = []
                        for datastream in batch["datastreams"]:
                            results[device_id].append({
                                "datastream_id": datastream["id"],
                                "status": "Failed",
                                "error": f"Request exceeded size limit ({self.max_request_size_bytes} bytes)"
                            })
                        continue

                    response = send_request(method='post', headers=self.headers, url=url, json_payload=batch)
                    for datastream in batch['datastreams']:
                        result = {
                            "datastream_id": datastream["id"],
                            "status": "Success" if response.status_code == 201 else "Failed",
                        }
                        if include_payload and response.status_code == 201:
                            result["payload"] = batch
                        if device_id not in results:
                            results[device_id] = []
                        results[device_id].append(result)
                    """
                        print("request_size",request_size)
                        print(f"Device ID: {device_id}")
                        print(f"Batch: {batch}")
                    """

            except Exception as e:
                errors.setdefault(device_id, []).append({"error": str(e)})

        if errors:
            print(f"Errors occurred: {errors}")
        return results


    def _add_datapoint_to_payload(self, device_id, datastream_id, datapoint):
        """
        Agrega un datapoint al datastream correspondiente.
        """
        device = self.payload['devices'][device_id]
        existing_ds = next(
            (ds for ds in device['datastreams'] if ds['id'] == datastream_id), None
        )

        if existing_ds:
            existing_ds['datapoints'].append(datapoint)
        else:
            device['datastreams'].append({"id": datastream_id, "datapoints": [datapoint]})



