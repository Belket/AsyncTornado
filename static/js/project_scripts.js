function uuid4(){
    let dt = new Date().getTime();
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function initialize(){
    session_uuid = uuid4();
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
            let error_code = data["error_code"];
            if (error_code === 0){
                let scores = data["scores"];
            }
            else if (error_code === 1) {
                $('#scores').html("Ошибка в аргументах");
            }
            else if (data === 2) {
                $('#scores').html("Запрос не существует");
            }
            else {
                $('#scores').html("Неизвестная ошибка");
            }
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
                console.log(error_code);
                if (error_code === 0){
                    let scores = data["scores"];
                    $('#scores').html();
                    $('#accuracy').innerHTML = scores["accuracy"];
                    $('#recall').innerHTML = scores["recall"];
                    $('#precision').innerHTML = scores["precision"];
                    $('#f_score').innerHTML = scores["f_score"];
                }
                else if (error_code === 1) {
                    $('#scores').html("Ошибка в аргументах");
                }
                else if (data === 2) {
                    $('#scores').html("Запрос не существует");
                }
                else {
                    $('#scores').html("Неизвестная ошибка");
                }
            }
        });
    }