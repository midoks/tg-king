// console.log("jj");

function funcList(){
	var f ='<div class="sfm-opt">\
            <button class="layui-btn layui-btn-primary layui-btn-sm" onclick="push_simple_msg();">推送文字信息</button>\
        </div>'; 
    $(".soft-man-con").html(f);
}

function push_simple_msg(){
    layer.open({
        area: ['400px'],
        title:'推送简单文字信息',
        content: '<form class="layui-form layui-form-pane pd15">\
            <div class="layui-form-item layui-form-text">\
              <label class="layui-form-label">消息</label>\
              <div class="layui-input-block">\
                <textarea name="msg" placeholder="大家好" class="layui-textarea"></textarea>\
              </div>\
            </div>\
        </form>',
        btn: ['推送','取消'],
        type: 1,
        shadeClose: false,
        success:function(){
            // form.render('select');
        },
        yes: function(index, layero){
            var msg = $('textarea[name="msg"]').val();
            modPost('clientmgr', 'push_text', {msg:msg}, function(data){
                var data = $.parseJSON(data.data);
            	console.log(data);
            	showMsg(data.msg,function(){
                    if (data.status){
                        layer.close(index);
                    }
                },{icon:data.status?1:2});
            })
            return;
        }
    });
}