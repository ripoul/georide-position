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

//

function onInput() {
    startDate = document.querySelector("#startDate");
    endDate = document.querySelector("#endDate");

    endDate.setCustomValidity(new Date(startDate.value) > new Date(endDate.value) ? "EndDate has to be after startDate." : "")
}
    