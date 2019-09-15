import os
import pprint
import numpy as np
import pandas as pd
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances

from utils.utils import timeit
from utils.path_utlis import project_root


def remove_tabs(df: pd.DataFrame):
    return df.drop(df.loc[df['key'] == 'Tab'].index)


def special2normal(df: pd.DataFrame):
    # TODO: add more special signs
    special_mapper = {'!': '1',
                      '@': '2',
                      '#': '3',
                      '$': '4',
                      '%': '5',
                      '^': '6',
                      '&': '7',
                      '*': '8',
                      '(': '9',
                      ')': '0',
                      '_': '-',
                      '+': '=',
                      '£': '§'}

    df.key = df.key.replace(special_mapper)
    return df


def transform_data(df: pd.DataFrame):
    new_df = pd.DataFrame(columns=['key', 'keydown', 'keyup'])
    df.key = df.key.apply(lambda x: x.lower())
    grouped = df.groupby('key').apply(lambda x: x.time)
    keys_time = grouped.values.reshape(-1, 2)
    keys_values = grouped.index.levels[0][grouped.index.codes[0]].values.reshape(-1, 1).astype(str)

    new_df['key'] = keys_values[:,0][::2]
    new_df['keydown'] = keys_time[:,0]
    new_df['keyup'] = keys_time[:,1]

    return new_df.sort_values('keydown').reset_index(drop=True)


def dwell_time(df, index):
    first_action = df.iloc[index].keydown
    second_action = df.iloc[index].keyup
    return second_action - first_action


def interval(df, index):
    first_action = df.iloc[index].keyup
    second_action = df.iloc[index+1].keydown
    return second_action - first_action


def flight_time(df, index):
    first_action = df.iloc[index].keydown
    second_action = df.iloc[index + 1].keydown
    return second_action - first_action


def up2up(df, index):
    first_action = df.iloc[index].keyup
    second_action = df.iloc[index+1].keyup
    return second_action - first_action


def latency(df, index):
    first_action = df.iloc[index].keydown
    second_action = df.iloc[index+1].keyup
    return second_action - first_action


def calculate_dwell_times(df: pd.DataFrame):
    return [dwell_time(df, i) for i in range(len(df))]


def calculate_intervals(df: pd.DataFrame):
    return [interval(df, i) for i in range(len(df)-1)]


def calculate_up2ups(df: pd.DataFrame):
    return [up2up(df, i) for i in range(len(df)-1)]


def calculate_latencies(df: pd.DataFrame):
    return [latency(df, i) for i in range(len(df)-1)]


def calculate_flight_times(df: pd.DataFrame):
    return [flight_time(df, i) for i in range(len(df)-1)]


def calculate_features(df: pd.DataFrame):
    features = {
        'dwell_times': np.array(calculate_dwell_times(df)).reshape(1, -1),
        'intervals': np.array(calculate_intervals(df)).reshape(1, -1),
        'up2up': np.array(calculate_up2ups(df)).reshape(1, -1),
        'flight_times': np.array(calculate_flight_times(df)).reshape(1, -1),
        'latencies': np.array(calculate_latencies(df)).reshape(1, -1)
        }
    return features


def calculate_distances(feat1, feat2):

    results = {
        key: {
            'manhattan': manhattan_distances(feat1[key], feat2[key]),
            'euclidean': euclidean_distances(feat1[key], feat2[key]),
        }
        for key in feat1.keys()
    }

    return results


# def return_feature_extractor():
#     return FeatureUnion([('dwell_times', FunctionTransformer(calculate_dwell_times, validate=False)),
#                          ('intervals', FunctionTransformer(calculate_intervals, validate=False)),
#                          ('up2up', FunctionTransformer(calculate_up2ups, validate=False)),
#                          ('flight_times', FunctionTransformer(calculate_flight_times, validate=False)),
#                          ('latencies', FunctionTransformer(calculate_latencies, validate=False))
#                          ])


def plot_features(feat1, feat2):
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(len(feat1), 1)
    fig.subplots_adjust(hspace=.5, wspace=.001)
    for cnt, feat in enumerate(feat1.keys()):
        axs[cnt].plot(feat1[feat][0])
        axs[cnt].plot(feat2[feat][0])
        axs[cnt].set_title(feat)

    plt.show()


@timeit
def main():
    data = pd.read_json(os.path.join(project_root(), 'local_tmp', 'file.json'))
    # feature_extractor = return_feature_extractor()
    pprinter = pprint.PrettyPrinter(indent=2, width=3)
    pipe = Pipeline(steps=[('remove_tabs', FunctionTransformer(remove_tabs, validate=False)),
                           ('special2normal', FunctionTransformer(special2normal, validate=False)),
                           ('reshape_matrix', FunctionTransformer(transform_data, validate=False)),
                           ('extract_feats', FunctionTransformer(calculate_features, validate=False)),
                           ], verbose=False)

    record2 = data[['record_2']]
    email2 = pd.DataFrame(record2.loc['email'][0])
    feat2 = pipe.fit_transform(email2)

    record3 = data[['record_3']]
    email3 = pd.DataFrame(record3.loc['email'][0])
    feat3 = pipe.fit_transform(email3)

    pprinter.pprint(calculate_distances(feat2, feat3))

    plot_features(feat2, feat3)


main()
