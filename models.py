
from server_information import ServerErrors
from objects import ServerModelsMethods
from modification_methods import dataset_preprocessing
import pandas as pd
import numpy as np
from copy import deepcopy
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class Models:

    def __init__(self):
        self.__models = {}
        self.initialization_process()

    def initialization_process(self):
        for method in ServerModelsMethods.methods:
            self.__models[method.model_id] = method

    @staticmethod
    def classification_scores(y_hat, y_test):
        scores = dict()
        scores["accuracy"] = accuracy_score(y_hat, y_test)
        scores["precision"] = precision_score(y_hat, y_test)
        scores["recall"] = recall_score(y_hat, y_test)
        scores["f_score"] = f1_score(y_hat, y_test)
        return scores

    def get_models(self):
        models_information = [model.model_information() for model in self.__models.values()]
        return models_information

    def read_df(self, df_name):
        try:
            path = "static/dataframes/" + df_name + ".csv"
            separator = ','
            df = pd.read_csv(path, sep=separator)
            return ServerErrors.NO_ERROR, df
        except:
            return ServerErrors.WRONG_INPUT_DATA, None

    def modify_df(self, df):
        try:
            dataset_preprocessing(df)
            return ServerErrors.NO_ERROR, df
        except:
            return ServerErrors.PROCESSING_ERROR, None

    def use_gscv(self, df, model):
        try:
            model_data = self.__models.get(model)
            model_object = model_data.sklearn_model
            parameters = model_data.parameters

            data = deepcopy(df)
            y = data['respiratory_disease']
            X = data.drop(['respiratory_disease'], axis=1)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
            classifier = GridSearchCV(model_object, parameters)
            classifier.fit(X_train, y_train)
            return ServerErrors.NO_ERROR, classifier.best_estimator_
        except:
            return ServerErrors.GSCV_ERROR, None

    def use_kfolds(self, df, best_estimator):
        model_score = {"accuracy": "", "precision": "", "recall": "", "f_score": ""}
        try:
            accuracies = []
            recalls = []
            precisions = []
            f_scores = []
            y = df['respiratory_disease']
            X = df.drop(['respiratory_disease'], axis=1)
            kf = KFold(n_splits=3, shuffle=True, random_state=123)
            for train_index, test_index in kf.split(X):
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]

                best_estimator.fit(X_train, y_train)
                y_hat = best_estimator.predict(X_test)
                model_score = Models.classification_scores(y_hat, y_test)
                accuracies.append(model_score.get("accuracy"))
                recalls.append(model_score.get("recall"))
                precisions.append(model_score.get("precision"))
                f_scores.append(model_score.get("f_score"))

            model_score = {"accuracy": np.mean(accuracies),
                           "precision": np.mean(precisions),
                           "recall": np.mean(recalls),
                           "f_score": np.mean(f_scores)}

            return ServerErrors.NO_ERROR, model_score
        except:
            return ServerErrors.KFOLDS_ERROR, model_score