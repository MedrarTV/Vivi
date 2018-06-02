/* $(function () {
    $.ajax({
        url: '{{ url_for("autocomplete") }}'
    }).done(function (data) {
        $('#selected_venue').autocomplete({
            source: data,
            minLength: 2
        });    
    });
}); */

/*
VARIABLES TO STORE THE IDS OF THE NEEDED DICTS
venue
artists
curator
interviewer
inst
videographer
event_type
title_of_edited_video
keywords
*/

console.log('HER    HER HER     Her');
var ids =[]

function AutoComplete(matchFieldName, resultFieldName, lookupURL) {
    $('#' + matchFieldName).autocomplete({
        source: function (request, response) {
            $.ajax({
                type: "GET",
                url: lookupURL,
                contentType: 'application/json',
                dataType: "json",
                data: JSON.stringify({ prefixText: request.term, count: 20 }),
                success: function (data) { 
                    console.log(request.term);                   
                    /* console.log(JSON.stringify(data));  
                    var output = $.makeArray(data);                                        
                    console.log(output); */
                    //var ids = []
                    response($.map(data, function (val,id) {
                        /* console.log(id)
                        console.log(val[1]) */
                        //ids.push(id);
                        return {
                            id : val[0],
                            value: val[1]
                            //label: (lab == lab) ? lab : lab + "(" + val + ")"
                        }
                    }));
                    ///console.log("IDS 1111  " + ids);
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    alert(textStatus);
                }
            });
        },
        minLength: 2,
        select: function (event, ui) {
            $('#' + resultFieldName).val(ui.item.value);
            ids.push(ui.item.id)
            console.log("the ids "+ids)
            return ui.item.id;
        }
    });
}