from server_information import ServerErrors, ServerCommands
from controller import Controller
from tornado.escape import json_decode
from json.decoder import JSONDecodeError
import os


class FileHandler(Controller):

    async def post(self):
        df_file = self.request.files['file'][0]
        session = self.request.headers["session"]
        extension = os.path.splitext(df_file['filename'])[1]
        final_filename = session + extension
        output_file = open("static/dataframes/" + final_filename, 'w')
        output_file.write(df_file['body'].decode())


class MainHandler(Controller):

    async def get(self):
        self.render("index.html",
                    filter_methods=self.processing.get_filter_methods(),
                    model_methods=self.models.get_models(),
                    balancing_methods=self.processing.get_balancing_methods())

    def post(self):

        try:
            request = json_decode(self.request.body)
            session = self.request.headers["session"]
            command, args = request["command"], request["args"]
        except (KeyError, JSONDecodeError):
            response = {"error_code": ServerErrors.MISS_ARG}
        else:
            if command == ServerCommands.FIT_MODEL:
                response = self.fit_model(args, session)
            else:
                response = {"error_code": ServerErrors.COMMAND_NOT_EXIST}
        finally:
            self.finish(response)

    def fit_model(self, args, session):
        try:
            filter_method, balancing_method, model = args["filter_method"], args["balancing_method"], args["model"]
        except KeyError:
            response = {"error_code": ServerErrors.MISS_ARG}
            return response
        print(filter_method, balancing_method, model)
        print(session)
        scores = {"accuracy": "", "recall": "", "precision": "", "f_score": ""}
        error_code, df = self.models.read_df(session)
        if error_code == ServerErrors.NO_ERROR:
            error_code, df = self.models.modify_df(df)
            if error_code == ServerErrors.NO_ERROR:
                error_code, df = self.processing.use_filter_method(df, filter_method)
                if error_code == ServerErrors.NO_ERROR:
                    error_code, df = self.processing.use_balancing_method(df, balancing_method)
                    if error_code == ServerErrors.NO_ERROR:
                        error_code, best_estimator = self.models.use_gscv(df, model)
                        if error_code == ServerErrors.NO_ERROR:
                            error_code, scores = self.models.use_kfolds(df, best_estimator)
        os.remove("static/dataframes/" + session + ".csv")
        return {"error_code": error_code, "scores": scores}

















