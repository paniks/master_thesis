import os
import pandas as pd
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer

from utils.utils import timeit
from utils.path_utlis import project_root


def remove_tabs(records: pd.DataFrame):
    return records.drop(records.loc[records['key'] == 'Tab'].index)


def transform_data(df: pd.DataFrame):
    new_df = pd.DataFrame(columns=['key', 'keydown', 'keyup'])
    grouped = df.groupby('key').apply(lambda x: x.time)
    keys_time = grouped.values.reshape(-1, 2)
    keys_values = grouped.index.levels[0][grouped.index.codes[0]].values.reshape(-1, 1).astype(str)

    new_df['key'] = keys_values[:,0][::2]
    new_df['keydown'] = keys_time[:,0]
    new_df['keyup'] = keys_time[:,1]

    return new_df.sort_values('keydown').reset_index(drop=True)


def dwell_time(records, index):
    first_action = records.iloc[index].keydown
    second_action = records.iloc[index].keyup
    return second_action - first_action


def interval(records, index):
    first_action = records.iloc[index].keyup
    second_action = records.iloc[index+1].keydown
    return second_action - first_action


def flight_time(records, index):
    first_action = records.iloc[index].keydown
    second_action = records.iloc[index + 1].keydown
    return second_action - first_action


def up2up(records, index):
    first_action = records.iloc[index].keyup
    second_action = records.iloc[index+1].keyup
    return second_action - first_action


def latency(records, index):
    first_action = records.iloc[index].keydown
    second_action = records.iloc[index+1].keyup
    return second_action - first_action


def calculate_dwell_times(records: pd.DataFrame):
    return [dwell_time(records, i) for i in range(len(records))]


def calculate_intervals(records: pd.DataFrame):
    return [interval(records, i) for i in range(len(records)-1)]


def calculate_up2ups(records: pd.DataFrame):
    return [up2up(records, i) for i in range(len(records)-1)]


def calculate_latencies(records: pd.DataFrame):
    return [latency(records, i) for i in range(len(records)-1)]


def calculate_flight_times(records: pd.DataFrame):
    return [flight_time(records, i) for i in range(len(records)-1)]


def return_feature_extractor():
    return FeatureUnion([('dwell_times', FunctionTransformer(calculate_dwell_times, validate=False)),
                         ('intervals', FunctionTransformer(calculate_intervals, validate=False)),
                         ('up2up', FunctionTransformer(calculate_up2ups, validate=False)),
                         ('flight_times', FunctionTransformer(calculate_flight_times, validate=False)),
                         ('latencies', FunctionTransformer(calculate_latencies, validate=False))
                         ])


@timeit
def main():
    data = pd.read_json(os.path.join(project_root(), 'local_tmp', 'file.json'))

    record = data[['record_0']]
    email = pd.DataFrame(record.loc['email'][0])
    feature_extractor = return_feature_extractor()

    pipe = Pipeline(steps=[('remove_tabs', FunctionTransformer(remove_tabs, validate=False)),
                           ('reshape_matrix', FunctionTransformer(transform_data, validate=False)),
                           ('extract_feats', feature_extractor)], verbose=True)

    pipe.fit_transform(email)

main()
