$(document).ready(function () {
    $('#example').DataTable({
        data: null,
        columns: [
            { title: "Tracker ID" },
            { title: "Tracker Name" }
        ]
    });
    $('#example').parents('div.dataTables_wrapper').first().hide();
});

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

$('#form_tracker').submit(function () {
    $.ajax({
        url: $('#form_tracker').attr('action'),
        type: 'POST',
        data: $('#form_tracker').serialize(),
        success: function (data) {
            $('#example').dataTable().fnClearTable();
            $('#example').dataTable().fnAddData(data);
            $('#example').parents('div.dataTables_wrapper').first().show();
        },
        error: function (e) {
            $('#modal_tracker').modal()
        }
    });
    return false;
});