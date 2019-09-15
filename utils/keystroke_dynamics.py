import pandas as pd
import json
import _io


def group_data_by_sourceid(data: pd.DataFrame) -> dict:
    return {i: data[data.sourceid.values == i].reset_index(drop=True) for i in pd.unique(data.sourceid.values)}


def log_values(data: pd.DataFrame, json_handler: _io.TextIOWrapper):

    log_file = json.load(json_handler)
    grouped_data = group_data_by_sourceid(data)

    element_idx = len(list(log_file.keys()))

    log_file.update({f'record_{element_idx}': {'email': grouped_data['email'].to_dict(orient='list'),
                                               'pwd': grouped_data['pwd'].to_dict(orient='list')}})
    json_handler.seek(0)
    json.dump(log_file, json_handler, sort_keys=True)
    json_handler.truncate()
