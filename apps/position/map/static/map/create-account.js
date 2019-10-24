$('#form').submit(function () {
    $.ajax({
        url: $('#form').attr('action'),
        type: 'POST',
        data: $('#form').serialize(),
        success: function (data) {
            window.location.href = "/trip/"+$('#id').val();
            return;
        },
        error: function (e) {
            $('#modal').modal()
            return;
        }
    });
    return false;
});

$("#token-info").tooltip({"placement": "right", "title": "Tokens are encrypted and stored in database. You can revoke a token using the Modifie Account page when you create an account."});

function onInput() {
    password = document.querySelector("#password");
    password2 = document.querySelector("#password2");
    startDate = document.querySelector("#startDate");
    endDate = document.querySelector("#endDate");

    password2.setCustomValidity(password2.value != password.value ? "Passwords do not match." : "")
    endDate.setCustomValidity(new Date(startDate.value) > new Date(endDate.value) ? "EndDate has to be after startDate." : "")
}
    
