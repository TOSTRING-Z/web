(function (global) {
    "use strict";
    //默认参数
    var plugin = {
        id: null,
        data: null,
        comment_url: null,
        huifu_url: null,
        loading: "loading",
        OwO: {
            body: null,
            api: "/static/js/OwO.json",
            detail_id: null,
            type: "comment",
        }
    };
    let owoUpdateType = function (type, detail_id, target_user_id) {
        if (type == "comment") {
            plugin.OwO.body[1].value = "comment";
            plugin.OwO.body[0].value = plugin.OwO.detail_id;
            plugin.OwO.body[3].value = 1;
        } else if (type == "comment_response") {
            plugin.OwO.body[1].value = "comment_response";
            plugin.OwO.body[0].value = detail_id;
            plugin.OwO.body[3].value = target_user_id;
        }
    };
    /** string **/
    String.prototype.format = function (args) {
        var result = this;
        if (arguments.length > 0) {
            if (arguments.length == 1 && typeof (args) == "object") {
                for (var key in args) {
                    if (args[key] != undefined) {
                        var reg = new RegExp("({" + key + "})", "g");
                        result = result.replace(reg, args[key]);
                    }
                }
            } else {
                for (var i = 0; i < arguments.length; i++) {
                    if (arguments[i] != undefined) {
                        var reg = new RegExp("({)" + i + "(})", "g");
                        result = result.replace(reg, arguments[i]);
                    }
                }
            }
        }
        return result;
    };

    function parseDom(arg) {
        var objE = document.createElement("div");
        objE.innerHTML = arg;
        return objE.childNodes[0];
    }

    function comment_init(json) {
        return '<div class="comment shadow-lg flex bg-white rounded-lg p-6">\
                    <img class="h-10 w-10 md:h-14 md:w-14 rounded-full mx-0 mr-6" src="/static/img/user/{user}.jpg" alt="{user}">\
                    <div class="text-left">\
                        <div class="text-gray-400">\
                            <span>{user} 发表于:{time}</span>\
                        </div>\
                        <div class="text-black">\
                            <p>{content}</p>\
                        </div>\
                        <div class="text-gray-400">\
                            <a class="comment-num cursor-pointer" data-detail-id="{detail_id}">{comment_num}条评论 <i class="ri-message-2-line cursor-pointer"></i></a>\
                            <a class="huiFu commend-response cursor-pointer" href="#owoTextarea" data-detail-id="{detail_id}" data-target-user-id="1">回复 <i class="ri-question-answer-line cursor-pointer"></i></a>\
                        </div>\
                    </div>\
                </div>'.format(json)
    }

    function huifu_init(json) {
        return '<div class="comment shadow-lg flex bg-white my-2 p-6">\
                    <img class="h-8 w-8 md:h-14 md:w-14 rounded-full mx-0 mr-6" src="/static/img/user/{user}.jpg" alt="{user}">\
                    <div class="text-left">\
                        <div class="text-gray-400">\
                            <span>{user} 发表于:{time}</span>\
                        </div>\
                        <div class="text-black">\
                            <p><b>@{target_user_name}:</b>{content}</p>\
                        </div>\
                        <div class="text-gray-400">\
                            <a class="huiFu commend-response" href="#owoTextarea" data-detail-id="{detail_id}" data-target-user-id="{target_user_id}">回复 <i class="ri-question-answer-line"></i></a>\
                        </div>\
                    </div>\
                </div>'.format(json).format(json)
    }

    function owo_init(json) {
        return '<form action="/owoSubmit" class="" id="owoTextarea" method="post">\
                    <a id="clear_response" class="cursor-pointer" style="display: none">取消回复<i class="ri-chat-delete-line ml-1"></i></a>\
                    <input type="hidden" value="{detail_id}" name="detail_id">\
                    <input type="hidden" value="{type}" name="type">\
                    <textarea contenteditable="true" name="content" class="OwO-textarea border border-gray-200 mt-6"></textarea>\
                    <input type="hidden" value="1" name="target_user_id">\
                    <div class="OwO"></div>\
                    <button class="OwO-button btn btn-primary pull-right" id="owoSubmit" type="button">发送</button>\
                    <p class="text-gray-600 mt-6" style="display: {p}">欢迎<a class="cursor-pointer text-gray-800 mr-2 ml-2" onclick=\'$("#owoUserInfo").css("display",$("#owoUserInfo").css("display")=="none"?"block":"none")\'>{user_name}</a>归来！</p>\
                    <div id="owoUserInfo" class="shadow-lg text-gray-900 flex bg-white rounded-lg p-6" style="display: {div}">\
                        <div class="flex mr-4">\
                            <label for="user_name" class="mr-4">名称<span class="text-blue-300">*</span></label>\
                            <div class="flex">\
                                <img class="h-8 w-8 rounded-full" src="/static/img/user/{user_name}.jpg" alt=" ">\
                                <input id="user_name" name="user_name" type="text" value="{user_name}" maxlength="245" placeholder="姓名或昵称">\
                            </div>\
                        </div>\
                        <div class="flex mr-4">\
                            <label for="email" class="mr-4">邮箱<span class="text-blue-300">*</span></label>\
                            <div class="flex">\
                                <input type="text" name="email" id="email" placeholder="邮箱 (必填,将保密)" value="{email}">\
                            </div>\
                        </div>\
                        <div class="flex mr-4">\
                            <label for="url" class="mr-4">地址&nbsp;&nbsp;</label>\
                            <div class="flex">\
                                <input id="web_site" name="web_site" type="url" value="{web_site}" maxlength="200" placeholder="网站或博客">\
                            </div>\
                        </div>\
                    </div>\
                </form>'.format(json)
    }

    let init = function (data, id) {

        var comment_body = parseDom('<div id="{}_body" class="text-sm text-gray-700 lg:my-8"></div>'.format({"id": id}));

        if (global.hasOwnProperty("OwO")) {
            plugin.OwO.body = parseDom(owo_init({
                "detail_id": plugin.OwO.detail_id,
                "type": plugin.OwO.type,
                "p": $.cookie('user_name') ? "block" : "none",
                "div": $.cookie('user_name') ? "none" : "block",
                "user_name": $.cookie('user_name') || "",
                "email": $.cookie('email') || "",
                "web_site": $.cookie('web_site') || ""
            }));
            document.getElementById(id).appendChild(plugin.OwO.body);
            var OwO_demo = new OwO({
                logo: 'OωO',
                target: plugin.OwO.body.children[3],
                container: plugin.OwO.body.children[5],
                api: plugin.OwO.api,
                position: 'down',
                width: '240px',
                maxHeight: '250px'
            });
            $("#owoSubmit").click(function () {
                $.ajax({
                    url: "/owoSubmit",
                    data: $('form[action="/owoSubmit"]').serialize(),
                    beforeSend: () => {
                        $.cookie('user_name', $('#user_name').val());
                        $.cookie('email', $('#email').val());
                        $.cookie('web_site', $('#web_site').val());
                        if (global.hasOwnProperty('refresh')) {
                            refresh();
                        } else {
                            location.reload()
                        }
                    },
                    complete: () => {
                        /*if(global.hasOwnProperty('refresh')){
                            refresh();
                        }else{
                            location.reload()
                        }*/
                    }
                })

            })
        }

        document.getElementById(id).appendChild(comment_body);

        function pageFresh() {
            comment_body.appendChild(parseDom("<div class='yum mt-6'>共有<b>{dataLength}</b>条评论</div>".format({"dataLength": data.length})));
            for (let key in data) {
                comment_body.appendChild((parseDom(comment_init(data[key]))));
            }
            $(".comment-num").click((e) => {
                plugin.comment(e)
            });
            $(".commend-response").click((e) => {
                owoUpdateType('comment_response', $(e.target).data("detail-id"), $(e.target).data("target-user-id"));
                $("#clear_response").css("display", "block");
            });
            $("#clear_response").click(() => {
                owoUpdateType('comment', null, null);
                $("#clear_response").css("display", "none");
            });
        }

        pageFresh();

    };
    plugin.comment = function (e) {
        var element = e.target;
        var detail_id = $(element).data("detail-id");
        $.ajax({
            url: plugin.huifu_url + "?detail_id=" + detail_id,
            beforeSend: function () {
                $("#" + plugin.loading).removeClass("hide");
            },
            dataType: "JSON",
            success: function (data) {
                var huifu_body = document.createElement('div');
                for (let key in data) {
                    huifu_body.appendChild(parseDom(huifu_init(data[key])));
                }
                if (!element.hasOwnProperty("hasClick")) {
                    element.hasClick = true;
                    element.parentElement.parentElement.appendChild(huifu_body);
                }
                $("#" + plugin.loading).addClass("hide");
                $(".commend-response").click((e) => {
                    owoUpdateType('comment_response', $(e.target).data("detail-id"), $(e.target).data("target-user-id"));
                    $("#clear_response").css("display", "block");
                });
            }
        })
    };

    function comment(plu) {
        plugin = (function (plu) {
            if (!plu) {
                return plugin
            } else {
                Object.keys(plu).forEach((key) => {
                    if (typeof (plu[key]) == "object") {
                        Object.keys(plu[key]).forEach((key1) => {
                            plugin[key][key1] = plu[key][key1];
                        })
                    } else {
                        plugin[key] = plu[key];
                    }
                });
                return plugin
            }
        })(plu);
        if (plugin.data) {
            init(plugin.data, plugin.id);
        } else {
            $.ajax({
                url: plugin.comment_url,
                dataType: "JSON",
                success: (data) => {
                    init(data, plugin.id);
                }
            })
        }
    }

    comment.prototype.owoUpdateType = owoUpdateType;
    comment.prototype.plugin = plugin;

    global.comment = comment;
})(this);

