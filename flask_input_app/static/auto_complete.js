$(function () {
    $.ajax({
        url: '{{ url_for("autocomplete") }}'
    }).done(function (data) {
        $('#selected_venue').autocomplete({
            source: data,
            minLength: 2
        });    
    });
});

alert("HER");