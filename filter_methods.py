from copy import deepcopy
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split


class FilterMethods:

    @staticmethod
    def filtering(data):
        df = deepcopy(data)
        X = df.drop(['respiratory_disease'], axis=1)  # Feature Matrix
        X.drop(["date1"], axis=1, inplace=True)
        correlation = df.corr()
        correlation_target = abs(correlation['respiratory_disease'])
        relevant_features = correlation_target[correlation_target > 0.05]
        relevant_features_names = relevant_features.index

        corr_matrix = df[relevant_features_names].corr().abs()

        # the matrix is symmetric so we need to extract upper triangle matrix without diagonal (k = 1)
        corr_pairs = (corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool)).stack().sort_values(ascending=False))
        extra_corr_pairs = corr_pairs[corr_pairs > 0.5]
        for pair in extra_corr_pairs.index:
            feature_1, feature_2 = pair
            if feature_1 in relevant_features and feature_2 in relevant_features:
                feature_1_relevant_corr = relevant_features[feature_1]
                feature_2_relevant_corr = relevant_features[feature_2]
                if feature_1_relevant_corr > feature_2_relevant_corr:
                    relevant_features.drop(feature_2, inplace=True)
                else:
                    relevant_features.drop(feature_1, inplace=True)
        df_preprocessed = data[relevant_features.index]
        return df_preprocessed

    @staticmethod
    def backward_elimination(data):
        df = deepcopy(data)
        y = df['respiratory_disease']
        X = df.drop(['respiratory_disease'], axis=1)  # Feature Matrix
        X.drop(["date1"], axis=1, inplace=True)
        columns = list(X.columns)
        pmax = 1
        while len(columns) > 0:
            p = []
            X_1 = X[columns]
            X_1 = sm.add_constant(X_1)
            model = sm.OLS(y, X_1).fit()
            p = pd.Series(model.pvalues.values[1:], index=columns)
            pmax = max(p)
            feature_with_p_max = p.idxmax()
            if pmax > 0.05:
                columns.remove(feature_with_p_max)
            else:
                break
        selected_features_BE = columns
        return data[selected_features_BE]

    @staticmethod
    def recursive_feature_elimination(data):
        df = deepcopy(data)
        y = df['respiratory_disease']
        X = df.drop(['respiratory_disease'], axis=1)  # Feature Matrix
        X.drop(["date1"], axis=1, inplace=True)
        model = LogisticRegression()  # Initializing RFE model
        rfe = RFE(model, 7)  # Transforming data using RFE
        X_rfe = rfe.fit_transform(X, y)  # Fitting the data to model
        model.fit(X_rfe, y)
        nof_list = np.arange(1, 13)
        high_score = 0
        # Variable to store the optimum features
        nof = 0
        score_list = []
        for n in range(len(nof_list)):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
            model = LogisticRegression()
            rfe = RFE(model, nof_list[n])
            X_train_rfe = rfe.fit_transform(X_train, y_train)
            X_test_rfe = rfe.transform(X_test)
            model.fit(X_train_rfe, y_train)
            score = model.score(X_test_rfe, y_test)
            score_list.append(score)
            if (score > high_score):
                high_score = score
                nof = nof_list[n]
        cols = list(X.columns)
        model = LogisticRegression()
        # Initializing RFE model
        rfe = RFE(model, 9)
        # Transforming data using RFE
        X_rfe = rfe.fit_transform(X, y)
        # Fitting the data to model
        model.fit(X_rfe, y)
        temp = pd.Series(rfe.support_, index=cols)
        selected_features_rfe = temp[temp == True].index
        return data[selected_features_rfe]