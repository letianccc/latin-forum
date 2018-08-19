


function fresh_social() {
    $( "#social" ).load(window.location.href + " #social>*" )
}

$("#social").on('click', 'button', function(e){
    follow_event = $('#social').has('.follow').length
    if (follow_event) {
        url = '{{ url_for('.follow') }}'
    } else {
        url = '{{ url_for('.unfollow') }}'
    }
    data = {
        'followed_id': {{ user.id }},
    }
    var posting = $.post(url, data, fresh_social)
    e.preventDefault()
})
