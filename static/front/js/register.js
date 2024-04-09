$(function () {
     $('#captcha-btn').click(function(event) {
        event.preventDefault(); // 阻止表单默认提交行为
        // 获取用户输入的邮箱地址
        var email = $('input[name="email"]').val();
        zlajax.get({
            url:"/user/mail/captcha?mail=" + email
        }).done(function (result){
            alert("验证码发送成功！")
        }).fail(function (error){
            alert(error.message)
        })
    });
});
