$('#form').submit(function () {
    $.ajax({
        url: $('#form').attr('action'),
        type: 'POST',
        data: $('#form').serialize(),
        success: function (data) {
            window.location.href = "/trip/" + $('#id').val();
            return;
        },
        error: function (e) {
            $('#modal').modal()
            return;
        }
    });
    return false;
});

//


$('#delete-user-btn').on("click", e => {
    e.preventDefault();
    $('#confirm-delete').modal();
});

$('#valid-delete-user').on("click", e => {
    $('#delete-user').submit();
});



function onInput() {
    startDate = document.querySelector("#startDate");
    endDate = document.querySelector("#endDate");

    endDate.setCustomValidity(new Date(startDate.value) > new Date(endDate.value) ? "EndDate has to be after startDate." : "")
}

$('#form_revoke_token').submit(function () {
    $.ajax({
        url: $('#form_revoke_token').attr('action'),
        type: 'POST',
        data: $('#form_revoke_token').serialize(),
        success: function (data) {
            $('#modal-revoke-token-ok').modal();
            return;
        },
        error: function (e) {
            $('#modal-revoke-token-ko').modal();
            return;
        }
    });
    return false;
});