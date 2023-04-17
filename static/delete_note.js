$(document).on('submit', 'form', function(event) {
    event.preventDefault(); // остановить отправку формы

    var form = $(this);
    var url = form.attr('action');
    var method = form.find('input[name="_method"]').val();

    $.ajax({
        url: url,
        type: 'POST',
        data: { _method: 'DELETE' },
        success: function(result) {
            // обработка успешного удаления заметки
        },
        error: function(xhr, status, error) {
            // обработка ошибки удаления заметки
        }
    });
});