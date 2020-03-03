####一个基于Django后台的评论插件

######初始化

```
<link href="tailwind.css" rel="stylesheet">
<link href="butterbar.css" rel="stylesheet">
<link href="OwO.min.css" rel="stylesheet">

<div id="loading" class="butterbar active hide">
    <span class="bar"></span>
</div>
<div id="content" class="content-wrapper py-32 lg:p-8 lg:w-3/4"></div>

<script src=jquery.cookie.js"></script>
<script src=OwO.min.js"></script>
<script src=comment.js"></script>
<script>
var mComment = new comment({
                    comment_url: '/comment/'+window.location.href.match(/\d+/g)[window.location.href.match(/\d+/g).length-1],
                    huifu_url: '/comment/huifu',
                    id: 'content',
                    loading:"loading",
                    OwO:{
                        api:"/static/js/OwO.json",
                        detail_id:window.location.href.match(/\d+/g)[window.location.href.match(/\d+/g).length-1],
                        type:"comment",
                    }
                });
</script>
```
