from copy import deepcopy
import pandas as pd
from sklearn.utils import resample


class BalancingMethods:

    @staticmethod
    def over_sampling(data):
        df = deepcopy(data)
        df_major = df[df.respiratory_disease == 1]
        df_minor = df[df.respiratory_disease == 0]
        df_minor_upsampled = resample(df_minor, replace=True, n_samples=df_major.shape[0])
        df_oversampled = pd.concat([df_major, df_minor_upsampled])
        return df_oversampled

    @staticmethod
    def under_sampling(data):
        df = deepcopy(data)
        df_major = df[df.respiratory_disease == 1]
        df_minor = df[df.respiratory_disease == 0]
        df_major_downsampled = resample(df_major, replace=True, n_samples=df_minor.shape[0])
        df_undersampled = pd.concat([df_minor, df_major_downsampled])
        return df_undersampled