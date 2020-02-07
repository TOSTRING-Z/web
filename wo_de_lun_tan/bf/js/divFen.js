//div分页
function divFen(id,data){
    //console.log(data);
    var id = id;
    var div = document.getElementById(id);
    var ul = document.getElementById(id+"_ul");


    var data = data;

    var dataLength = data.length;
    var curPage = 1;
    var pageRow = 24;
    var pageAll = parseInt(dataLength/pageRow)<dataLength/pageRow?parseInt(dataLength/pageRow+1):parseInt(dataLength/pageRow);
    function pageFresh() {
        ul.innerHTML = '';
        curPage = parseInt(curPage);
        var start = (curPage-1)*pageRow;
        var end = dataLength>curPage*pageRow?curPage*pageRow:dataLength;
        //div
        var h = '';
        for (let i = start;i < end; i ++) {
            var row = data[i];
            Object.keys(row).forEach(function (key) {
            h += row[key];
            })
        }
        div.innerHTML = h;
        //分页按钮

        var li_previous = document.createElement("li");
        var a_previous = document.createElement("a");
        a_previous.innerHTML = "«";
        a_previous.id = "«";
        li_previous.appendChild(a_previous);
        ul.appendChild(li_previous);
        if (pageAll <= 5) {
            for (let i = 1;i <= pageAll;i ++) {
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = i.toString();
                a.id = id+i.toString();
                li.appendChild(a);
                ul.appendChild(li);
            }
        }
        else {
            if (curPage <= 3) {
                for (let i = 1; i <= 4; i++) {
                    var li = document.createElement("li");
                    var a = document.createElement("a");
                    a.innerHTML = i.toString();
                    a.id = id+i.toString();
                    li.appendChild(a);
                    ul.appendChild(li);
                }
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = "...";
                li.appendChild(a);
                ul.appendChild(li);
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = pageAll;
                a.id = id+pageAll.toString();
                li.appendChild(a);
                ul.appendChild(li);
            }
            else if (curPage >= pageAll-2) {
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = 1;
                a.id = id+"1";
                li.appendChild(a);
                ul.appendChild(li);
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = "...";
                li.appendChild(a);
                ul.appendChild(li);
                for (let i = pageAll-3;i <= pageAll;i ++) {
                    var li = document.createElement("li");
                    var a = document.createElement("a");
                    a.innerHTML = i;
                    a.id = id+i.toString();
                    li.appendChild(a);
                    ul.appendChild(li);
                }
            }
            else {
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = 1;
                a.id = id+"1";
                li.appendChild(a);
                ul.appendChild(li);
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = "...";
                li.appendChild(a);
                ul.appendChild(li);
                //console.log(curPage);
                for (let i = curPage-1;i <= curPage+1;i ++) {
                    var li = document.createElement("li");
                    var a = document.createElement("a");
                    a.innerHTML = i;
                    a.id = id+i.toString();
                    li.appendChild(a);
                    ul.appendChild(li);
                }
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = "...";
                li.appendChild(a);
                ul.appendChild(li);
                var li = document.createElement("li");
                var a = document.createElement("a");
                a.innerHTML = pageAll;
                a.id = id+pageAll.toString();
                li.appendChild(a);
                ul.appendChild(li);
            }
        }
        var li_next = document.createElement("li");
        var a_next = document.createElement("a");
        a_next.innerHTML = "»";
        a_next.id = "»";
        li_next.appendChild(a_next);
        ul.appendChild(li_next);
        $("#"+id+"_ul li").attr("class","page-item");
        $("#"+id+"_ul a").attr("class","page-link");
        $("#"+id+"_ul a").attr("href","#");
        document.getElementById(id+curPage.toString()).parentElement.className = "page-item active";
        ul.onclick = function (e) {
            if (e.target.nodeName == "A"&&e.target.innerHTML !="...") {
                switch (e.target.innerHTML) {
                    case '«':
                        curPage = curPage>1?curPage-1:1;
                        break;
                    case '»':
                        curPage = curPage==pageAll?curPage:curPage+1;
                        break;
                    default:
                        curPage = e.target.innerHTML;
                        break;
                }
                pageFresh();
            }
        };
    }
    pageFresh();
}
