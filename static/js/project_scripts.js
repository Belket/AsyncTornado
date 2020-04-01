
function uuid4(){
    let dt = new Date().getTime();
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function error_alert(message){
    $('#mistake').html(message);
    $('#accuracy').html("");
    $('#recall').html("");
    $('#precision').html("");
    $('#f_score').html("");
}

function initialize(){
    session_uuid = uuid4();

    NO_ERROR = 0;
    MISS_ARG = 1;
    COMMAND_NOT_EXIST = 2;
    WRONG_INPUT_DATA = 3;
    PROCESSING_ERROR = 4;
    FILTERING_ERROR = 5;
    BALANCING_ERROR = 6;
    GSCV_ERROR = 7;
    KFOLDS_ERROR = 8;

}

function load_df() {
    let formData = new FormData(document.forms.df_form);
    let df = $('#data_frame').prop('files')[0];
    df['session'] = session_uuid;
    formData.append( 'file', df);

    $.ajax({
        method: "POST", // метод HTTP, используемый для запроса
        beforeSend: function(request) {request.setRequestHeader("session", session_uuid);},
        url: "/upload_file",
        dataType: 'text',
        cache: false,
        contentType: false,
        processData: false,
        data: formData,
        error: function () {
            $('#scores').text("Запрос не может быть обработан");
        },
        success: function (data) {
            console.log("Файл отправлен");
        }
    });
}


function fit_model(){
        let command = "fit_model";
        let filter_method = $("#filter_method").val();
        let balancing_method = $('#balancing_method').val();
        let model = $('#model_method').val();
        let args = {
            "filter_method": filter_method,
            "balancing_method": balancing_method,
            "model": model,
        };

        $.ajax({
            method: "POST", // метод HTTP, используемый для запроса
            beforeSend: function(request) {request.setRequestHeader("session", session_uuid);},
            url: "/",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({"command": command, "args": args}),
            async: false,
            error: function () {
                $('#scores').text("Запрос не может быть обработан");
            },

            success: function (data) {
                console.log("SUCCESS0");
                let error_code = data["error_code"];
                console.log(data);


                if (error_code === NO_ERROR){
                    let scores = data["scores"];
                    $('#mistake').html("");
                    $('#accuracy').html("Доля правильных ответов: " + scores["accuracy"]);
                    $('#recall').html("Точность: " + scores["recall"]);
                    $('#precision').html("Полнота: " + scores["precision"]);
                    $('#f_score').html("F мера: " + scores["f_score"]);
                }
                else if (error_code === MISS_ARG) {
                    error_alert("Ошибка в аргументах");
                }
                else if (error_code === COMMAND_NOT_EXIST) {
                    error_alert("Команда не существует");
                }
                else if (error_code === WRONG_INPUT_DATA) {
                    error_alert("Неверные входные данные");
                }
                else if (error_code === PROCESSING_ERROR) {
                    error_alert("Ошибка предобработки данных, проверьте входные данные");
                }
                else if (error_code === FILTERING_ERROR) {
                    error_alert("Ошибка методов фильтрации, попробуйте воспользоваться другим методом");
                }
                else if (error_code === BALANCING_ERROR) {
                    error_alert("Ошибка балансировки классов, попробуйте воспользоваться другим методом");
                }
                else if (error_code === GSCV_ERROR) {
                    error_alert("Ошибка в подборе параметров, попробуйте воспользоваться другой моделью");
                }
                else if (error_code === KFOLDS_ERROR) {
                    error_alert("Ошибка в обучении модели, попробуйте воспользоваться другой моделью");
                }
                else {
                    error_alert("Неизвестная ошибка");
                }
            }
        });
    }