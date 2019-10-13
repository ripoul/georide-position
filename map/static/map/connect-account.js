$('#form').submit(function () {
    $.ajax({
        url: $('#form').attr('action'),
        type: 'POST',
        data: $('#form').serialize(),
        success: function (data) {
            //redirect to road trip
            return;
        },
        error: function (e) {
            $('#modal').modal()
            return;
        }
    });
    return false;
});