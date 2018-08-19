


function fresh_social() {
    $( "#social" ).load(window.location.href + " #social>*" )
}


$(".follow").click(function(e){
    url = '{{ url_for('.follow') }}'
    data = {
        'followed_id': {{ user.id }},
    }
    var posting = $.post(url, data, fresh_social)
    e.preventDefault()
})
