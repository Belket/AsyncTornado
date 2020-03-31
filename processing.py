from server_information import ServerErrors
from objects import ServerFilterMethods, ServerBalancingMethods


class ProcessingMethods:

    def __init__(self):
        self.__filter_methods = {}
        self.__balancing_methods = {}
        self.initialization_process()

    def initialization_process(self):
        self.__filter_methods = {method.method_id: method for method in ServerFilterMethods.filter_methods}
        self.__balancing_methods = {method.method_id: method for method in  ServerBalancingMethods.balancing_methods}

    def get_filter_methods(self):
        filter_methods_information = [method.filter_method_information() for method in self.__filter_methods.values()]
        return filter_methods_information

    def get_balancing_methods(self):
        balancing_methods_information = [method.balancing_method_information() for method in self.__balancing_methods.values()]
        return balancing_methods_information

    def use_filter_method(self, df, filter_method):
        filter_object = self.__filter_methods.get(filter_method)
        df = filter_object.method(df)
        return ServerErrors.NO_ERROR, df

    def use_balancing_method(self, df, balancing_method):
        try:
            balancing_method = self.__balancing_methods.get(balancing_method)
            df = balancing_method.method(df)
            return ServerErrors.NO_ERROR, df
        except:
            return ServerErrors.BALANCING_ERROR, None
