
console.log('HER    HER HER     Her');




function AddKeyword(itemUrl, itemVal) {
	if(itemVal.length == 0){
		return;
	}
    $.ajax({
        type: "POST",
        url: itemUrl,
//        data: JSON.stringify(itemVal, null, '\t'),
        data: JSON.stringify(itemVal),
        contentType: 'application/json;charset=UTF-8',
        success: function () {
            alert(itemVal + ' added!');
            window.location.reload();
        },
        error: function(){
            alert('Error!!!')
        }
        
    });
    console.log(itemVal);
 }



function AddTopic() { }
function AddCategory() { }
function AddEventType(){}



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