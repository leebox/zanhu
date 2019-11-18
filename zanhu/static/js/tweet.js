$(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // 发布新动态
    $("#postNewTweetBtn").click(function(){
        $.ajax({
            url: "/post_new_tweet",
            data:$("#postNewTweetForm").serialize(),
            type: 'POST',
            cache: false,
            success: function(result){
                  // $("#tweet_stream").prepend(result);
                  $("#content").val("");
                  $('#exampleModal').modal('hide');
                  location.reload();
            },
            error: function (result) {
                alert(result.responseText);
            },
        });
    });
    // 获取当前删除按钮的动态PK
    let cur_pk;
    $('#tweet_stream .media').on('click', "#deleteTweetBtn", function () {
        cur_pk = $(this).parent().parent().attr('id');
    });
    // 删除动态
    $("#postDeleteTweetBtn").click(function(){
        $.ajax({
            url: "/delete/"+cur_pk,
            data:$("#deleteTweetForm").serialize(),
            type: 'POST',
            cache: false,
            success: function(result){
                  $('#deleteTweetModal').modal('hide');
                  location.reload();
            },
            error: function (result) {
                alert(result.responseText);
            },
        });
    });
    // 点赞动态
    $("#tweet_stream").on('click', "#likeTweetBtn", function(){
        var pk = $(this).parent().parent().attr('id');
        var span = $(this).children();
        $.ajax({
            url: "/like/",
            data:{'pk': pk, 'csrf_token': csrftoken},
            type: 'POST',
            cache: false,
            success: function(result){
                if($(span).hasClass('heart')){
                    $(span).html("&#xe698; " + result.total_like);
                    $(span).removeClass('heart')
                }
                else{
                    $(span).addClass( "heart" );
                    $(span).html("&#xe738; " + result.total_like);
                }
            },
            error: function (result) {
                alert(result.responseText);
            },
        });
    });
    // 显示评论列表
    $('.collapse').on('show.bs.collapse', function () {
            var pk = $(this).parent().attr('id');
            var part = $(this);
            $.ajax({
                url: "/comment/list/",
                data:{'pk': pk},
                type: 'GET',
                cache: false,
                beforeSend:function(){
                    $(".loading").show();
                },
                success: function(result){
                    $('.comment-list').empty();
                    $('.comment-list').append(result.html);
                    //把按钮的名字和ID换掉
                    // $(part).prev().$('span').html("&#xea5a; 收起评论");
                },
                complete:function(){
                    $(".loading").hide();
                },
                error: function (result) {
                    alert(result.responseText);
                },
            });
    });
    // 发布新评论
    $("#tweet_stream").on('click', "#postNewCommentBtn", function(){
        var form = $(this).closest('form');
        $.ajax({
            url: "/post_new_comment/",
            data: form.serialize(),
            type: 'POST',
            cache: false,
            success: function(result){
                  // // $("#tweet_stream").prepend(result);
                  $('textarea#postNewCommentContent').val('');
                  // $('#exampleModal').modal('hide');
                  location.reload();
            },
            error: function (result) {
                alert(result.responseText);
            },
        });
    });




});
