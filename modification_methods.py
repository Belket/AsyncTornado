from collections import Counter
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import pandas as pd


def appropriate_strings(df_without_none, string_with_nan, distance_metrics):
    most_appropriate_indexes = {}
    for distance_metric in distance_metrics:
        string_distances = distance_metric(string_with_nan.values.reshape(1, -1), df_without_none)
        string_distances = string_distances.reshape(string_distances.shape[1], )
        min_distance_string_index = np.where(string_distances == min(string_distances))[0][0]
        most_appropriate_indexes.update({distance_metric.__name__: min_distance_string_index})
    counter = Counter(most_appropriate_indexes.values())
    return {"appropriate_indexes": most_appropriate_indexes, "best_index": counter.most_common(1)[0][0]}


def replace_all_nan_by_values_from_closest_vector(df, distance_metrics):
    # creation of dataset without nan values
    df["index"] = df.index  # create column which will duplicate indexes to drop and restore rows with nan
    columns_with_nan = [column for column in df.columns if np.sum(df[column].isnull()) != 0]  # find columns with nan
    df_without_none = df.drop(df[columns_with_nan], axis=1)  # create dataset without columns with nan

    # finding list of all possible nan indexes and dict of column with nan and its indexes
    all_nan_indexes = set()
    for column_with_nan in columns_with_nan:
        nan_indexes = set(sum(np.argwhere(pd.isnull(df[column_with_nan])).tolist(), []))
        all_nan_indexes = all_nan_indexes.union(nan_indexes)
    all_nan_indexes = list(all_nan_indexes)  # list of indexes of strings with nan

    strings_with_nan = {}  # dict with strings with nan to restore them after finding the closest one
    for nan_index in all_nan_indexes:
        strings_with_nan.update({nan_index: df_without_none.loc[nan_index]})
    df_without_none.drop(df_without_none.index[all_nan_indexes], inplace=True, axis=0)
    df_without_none.reset_index(inplace=True, drop=True)  # reset indexes in a row

    # change nan values of original dataset
    for nan_index in all_nan_indexes:
        prepared_string = strings_with_nan[nan_index]  # take string with nan values to find the closest one
        best_string_index = appropriate_strings(df_without_none, prepared_string, distance_metrics)["best_index"]
        string_with_nan = df.loc[nan_index]  # string in which nan values will be found and replaced
        real_best_index = int(df_without_none.loc[best_string_index]["index"])  # index from original dataset
        closest_string = df.loc[real_best_index]  # the closest string from dataset without nan strings
        for column_with_nan in columns_with_nan:
            if pd.isnull(string_with_nan[column_with_nan]):
                df.loc[nan_index, column_with_nan] = closest_string[column_with_nan]  # set value
    df.drop(['index'], inplace=True, axis=1)


def dataset_preprocessing(df, distance_metrics=[euclidean_distances]):
    date_column = df.date1
    df.drop(["date1"], inplace=True, axis=1)
    replace_all_nan_by_values_from_closest_vector(df, distance_metrics)
    df["date1"] = date_column