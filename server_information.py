
class ServerErrors:
    NO_ERROR = 0
    MISS_ARG = 1
    COMMAND_NOT_EXIST = 2
    WRONG_INPUT_DATA = 3
    PROCESSING_ERROR = 4
    FILTERING_ERROR = 5
    BALANCING_ERROR = 6
    GSCV_ERROR = 7
    KFOLDS_ERROR = 8


class ServerCommands:
    GET_MODELS = "get_models"
    GET_FILTER_METHODS = "get_filter_methods"
    GET_BALANCING_METHODS = "get_balancing_methods"
    FIT_MODEL = "fit_model"
    LOAD_DF = "load_df"






