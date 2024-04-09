$(function (){
    var editor = new window.wangEditor("#editor");
    editor.create();
    $('#submit-btn').click(function(event) {
        event.preventDefault(); // 阻止表单默认提交行为
        // 获取用户输入的邮箱地址
        var title = $('input[name="title"]').val();
        var board_id = $("select[name='board_id']").val();
        var content = editor.txt.html()

        zlajax.post({
            url:"/post/public",
            data:{title,board_id,content}
        }).done(function (data){
           setTimeout(function (){
               window.location="/";
           },2000);
        }).fail(function (error){
            alert(error.message)
        });
    });
});