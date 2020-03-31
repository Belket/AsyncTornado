from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from balancing_methods import BalancingMethods
from filter_methods import FilterMethods
import uuid


class FilterMethod:

    def __init__(self, method_id, method_name, method):
        self.method_id = method_id
        self.__method_name = method_name
        self.method = method

    def filter_method_information(self):
        return {"filter_method_id": self.method_id, "filter_method_name": self.__method_name}


class BalancingMethod:

    def __init__(self, method_id, method_name, method):
        self.method_id = method_id
        self.__method_name = method_name
        self.method = method

    def balancing_method_information(self):
        return {"balancing_method_id": self.method_id, "balancing_method_name": self.__method_name}

    def use_method(self, df):
        self.method(df)


class Model:
    def __init__(self, model_id, model_name, sklearn_model, parameters):
        self.model_id = model_id
        self.__model_name = model_name
        self.sklearn_model = sklearn_model
        self.parameters = parameters

    def model_information(self):
        return {"model_method_id": self.model_id, "model_method_name": self.__model_name}


class ServerFilterMethods:

    filter_methods = [
        FilterMethod(str(uuid.uuid4()), "Фильтрация", FilterMethods.filtering),
        FilterMethod(str(uuid.uuid4()), "backward_elimination", FilterMethods.backward_elimination),
        FilterMethod(str(uuid.uuid4()), "recursive_feature_elimination", FilterMethods.recursive_feature_elimination)
    ]


class ServerBalancingMethods:

    balancing_methods = [
        BalancingMethod(str(uuid.uuid4()), "UnderSampling", BalancingMethods.under_sampling),
        BalancingMethod(str(uuid.uuid4()), "OverSampling", BalancingMethods.over_sampling)
    ]


class ServerModelsMethods:

    methods = [
        Model(str(uuid.uuid4()), "Логистическая регрессия", LogisticRegression(), {'penalty': ('l2',), 'C': [1, 10], 'solver': ('newton-cg', 'lbfgs', 'liblinear')}),
        Model(str(uuid.uuid4()), "Дерево решений", DecisionTreeClassifier(), {'criterion': ('gini', 'entropy'), 'max_depth': (2, 5, 10), 'max_features': (3, 6, 9)}),
        Model(str(uuid.uuid4()), "Метод опорных векторов", SVC(),     {'kernel': ('rbf', 'sigmoid'), 'C': [1, 10]}),
        Model(str(uuid.uuid4()), "Линейный метод опорных векторов", LinearSVC(), {'penalty': ('l2',), 'C': [1, 10]}),
        Model(str(uuid.uuid4()), "k ближайших соседей", KNeighborsClassifier(), {'algorithm': ('auto', 'ball_tree', 'kd_tree', 'brute'), 'n_neighbors': (5, 10, 15, 50)}),
        Model(str(uuid.uuid4()), "Случайный лес", RandomForestClassifier(), {'criterion': ('gini', 'entropy'), 'max_depth': (2, 5, 10), 'n_estimators': (50, 100, 200)})
    ]






