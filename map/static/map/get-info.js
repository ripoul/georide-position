$('#form_token').submit(function () {
    $.ajax({
        url: $('#form_token').attr('action'),
        type: 'POST',
        data: $('#form_token').serialize(),
        success: function (data) {
            $('#token').val(data.token);
            return;
        },
        error: function (e) {
            $('#modal_token').modal()
            return;
        }
    });
    return false;
});

$("#copy-token").on("click", function (event) {
    $("#token").select();
    document.execCommand("copy");
});