

function showMsg(msg, callback ,icon, time){

	if (typeof time == 'undefined'){
		time = 2000;
	}

	if (typeof icon == 'undefined'){
		icon = {};
	}

	var loadT = layer.msg(msg, icon);
	setTimeout(function() {
		layer.close(loadT);
		if (typeof callback == 'function'){
			callback();
		}
	}, time);
}


function msgTpl(msg, args){
	if (typeof args == 'string'){
		return msg.replace('{1}', args);
	} else if (typeof args == 'object'){
		for (var i = 0; i < args.length; i++) {
			rep = '{' + (i + 1) + '}';
			msg = msg.replace(rep, args[i]);
		}	
	}
	return msg;
}

function modPost(module_name, func_name, args, succ_func){
    $.post("/module/run", {name:module_name,func:module_name,args:args}, function(data) {
        succ_func(data);
    },'json')
}

function modService(_name, version){
	var data = {name:_name, func:'status'}
	if ( typeof(version) != 'undefined' ){
		data['version'] = version;
	} else {
		version = '';
	}
	// console.log(version);

	var loadT = layer.msg('正在获取...', { icon: 16, time: 0, shade: 0.3 });
	$.post('/module/run', data, function(data) {
		layer.close(loadT);
        if(!data.status){
            layer.msg(data.msg,{icon:0,time:3000,shade: [0.3, '#000']});
            return;
        }
        if (data.data == 'start'){
            modSetService(_name, true, version);
        } else {
            modSetService(_name, false, version);
        }
    },'json');
}

function modSetService(_name ,status, version){
	var serviceCon ='<p class="status">当前状态：<span>'+(status ? '开启' : '关闭' )+
        '</span><span style="color: '+
        (status?'#20a53a;':'red;')+
        ' margin-left: 3px;" class="glyphicon ' + (status?'glyphicon glyphicon-play':'glyphicon-pause')+'"></span></p><div class="sfm-opt">\
            <button class="layui-btn layui-btn-primary layui-btn-sm" onclick="modOpService(\''+_name+'\',\''+(status?'stop':'start')+'\')">'+(status?'停止':'启动')+'</button>\
            <button class="layui-btn layui-btn-primary layui-btn-sm" onclick="modOpService(\''+_name+'\',\'restart\')">重启</button>\
            <button class="layui-btn layui-btn-primary layui-btn-sm" onclick="modOpService(\''+_name+'\',\'reload\')">重载配置</button>\
        </div>'; 
    $(".soft-man-con").html(serviceCon);
}


function modOpService(a, b) {

    var c = "name=" + a + "&func=" + b;

    var d = "";
    switch(b) {
        case "stop":d = '停止';break;
        case "start":d = '启动';break;
        case "restart":d = '重启';break;
        case "reload":d = '重载';break;
    }
    layer.confirm( msgTpl('您真的要{1}{2}服务吗？', [d,a]), {icon:3,closeBtn: 1}, function() {
        var e = layer.msg(msgTpl('正在{1}{2}服务,请稍候...',[d,a]), {icon: 16,time: 0});
        $.post("/module/run", c, function(g) {
            layer.close(e);
          
            var f = g.data == 'ok' ? msgTpl('{1}服务已{2}',[a,d]) : msgTpl('{1}服务失败!',[a,d]);
            layer.msg(f, {icon: g.data == 'ok' ? 1 : 2});
            
            if( b != "reload" && g.data == 'ok' ) {
                if ( b == 'start' ) {
                    modSetService(a, true, v);
                } else if ( b == 'stop' ){
                    modSetService(a, false, v);
                }
            }

            if( g.status && g.data != 'ok' ) {
                layer.msg(g.data, {icon: 2,time: 3000,shade: 0.3,shadeClose: true});
            }

            setTimeout(function(){
            	console.log('module run');
            },2000);
        },'json').error(function() {
            layer.close(e);
            layer.msg('操作异常!', {icon: 1});
        });
    })
}



function modInitD(_name){
	var loadT = layer.msg('正在获取...', { icon: 16, time: 0, shade: 0.3 });
	$.post('/module/run', {name:_name, func:'initd_status'}, function(data) {
		layer.close(loadT);
        if( !data.status ){
            layer.msg(data.msg,{icon:0,time:3000,shade: [0.3, '#000']});
            return;
        }
        if( data.data!='ok' && data.data!='fail' ){
            layer.msg(data.data,{icon:0,time:3000,shade: [0.3, '#000']});
            return;
        }
        if (data.data == 'ok'){
            modSetInitD(_name, true);
        } else {
            modSetInitD(_name, false);
        }
    },'json');
}

function modSetInitD(_name, status){
	var serviceCon ='<p class="status">当前状态：<span>'+(status ? '已加载' : '未加载' )+
        '</span><span style="color: '+
        (status?'#20a53a;':'red;')+
        ' margin-left: 3px;" class="glyphicon ' + (status?'glyphicon glyphicon-play':'glyphicon-pause')+'"></span></p><div class="sfm-opt">\
            <button class="layui-btn layui-btn-primary layui-btn-sm" onclick="modOpInitD(\''+_name+'\',\''+(status?'initd_uninstall':'initd_install')+'\')">'+(status?'卸载':'加载')+'</button>\
        </div>'; 
    $(".soft-man-con").html(serviceCon);
}

function modOpInitD(a, b) {
    var c = "name=" + a + "&func=" + b;
    var d = "";
    switch(b) {
        case "initd_install":d = '加载';break;
        case "initd_uninstall":d = '卸载';break;
    }
    layer.confirm( msgTpl('您真的要{1}{2}服务吗？', [d,a]), {icon:3,closeBtn: 1}, function() {
        var e = layer.msg(msgTpl('正在{1}{2}服务,请稍候...',[d,a]), {icon: 16,time: 0});
        $.post("/module/run", c, function(g) {
            layer.close(e);
            var f = g.data == 'ok' ? msgTpl('{1}服务已{2}',[a,d]) : msgTpl('{1}服务{2}失败!',[a,d]);
            layer.msg(f, {icon: g.data == 'ok' ? 1 : 2});
            
            if ( b == 'initd_install' && g.data == 'ok' ) {
                modSetInitD(a, true);
            }else{
                modSetInitD(a, false);
            }
            if(g.data != 'ok') {
                layer.msg(g.data, {icon: 2,time: 0,shade: 0.3,shadeClose: true});
            }
        },'json').error(function() {
            layer.close(e);
            layer.msg('系统异常!', {icon: 0});
        });
    })
}

function modLogs(_name, func, line){
	var _this = this;

    var func_name = 'error_log';
    if ( typeof(func) != 'undefined' ){
        func_name = func;
    }

    var file_line = 100;
    if ( typeof(line) != 'undefined' ){
        file_line = line;
    }


    var loadT = layer.msg('日志路径获取中...',{icon:16,time:0,shade: [0.3, '#000']});
    $.post('/module/run', {name:_name, func:func_name},function (data) {
        layer.close(loadT);

        try{
        	var jdata = $.parseJSON(data.data);
        	if (!jdata['status']){
        		layer.msg(jdata.msg,{icon:0,time:2000,shade: [0.3, '#000']});
                return;
        	}
		}catch(err){/*console.log(err);*/}


        var loadT2 = layer.msg('文件内容获取中...',{icon:16,time:0,shade: [0.3, '#000']});
        var fileName = data.data;
        $.post('/module/get_last_body', 'path=' + fileName+'&line='+file_line, function(rdata) {
            layer.close(loadT2);
            if (!rdata.status){
                layer.msg(rdata.msg,{icon:0,time:2000,shade: [0.3, '#000']});
                return;
            }
            
            if(rdata.data == '') {
            	rdata.data = '当前没有日志!';
            }
     
            var h =  parseInt($('.tg-w-menu').css('height')) - 40;
            var ebody = '<textarea readonly style="margin: 0px;height: '+h+'px;width: 100%;background-color: #333;color:#fff; padding:0 5px" id="info_log">'+rdata.data+'</textarea>';
            $(".soft-man-con").html(ebody);
            var ob = document.getElementById('info_log');
            ob.scrollTop = ob.scrollHeight; 
        },'json');
    },'json');
}


