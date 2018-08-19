

function show_response_form() {
    interact = $(this).parents('.comment-interact')
    comment_form = interact.next()
    comment_form.css('display', 'block')
    interact.css('display', 'none')
}

function hide_response_form(comment_form) {
    comment_form.css('display', 'none')
    interact = comment_form.prev()
    interact.css('display', 'block')
}

$(".response").click(show_response_form)

$(".cancle_comment").click(function(){
    comment_form = $(this).parents('.comment_form')
    comment_form.css('display', 'none')
    interact = comment_form.prev()
    interact.css('display', 'block')
    return false
});

$(".comment").hover(function(){
    $(this).find('.interact').css('visibility', 'visible')
});

$(".comment").mouseleave(function(){
    $(this).find('.interact').css('visibility', 'hidden')
});

$('.comment_form').submit(function (e) {
    form = $(this)
    url = form.attr( "action" );
    data = form.serialize()
    var posting = $.post( url, data, function() {
        need_hide = form.find('.cancle_comment').length != 0
        if (need_hide) {
            hide_response_form(form)
        }
        form.trigger("reset")
    });

    e.preventDefault();

});

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
        }
    }
})
