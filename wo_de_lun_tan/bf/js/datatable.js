//表格分页
function table(id,data){
    var id = id;
    //var sort_th = document.getElementById(id).children[0].children[0].children;
    //console.log(sort_th);
    var tbody = document.getElementById(id).children[1];
    var ul = document.getElementById(id+"_ul");

    var data = data;

    var dataLength = data.length;
    var curPage = 1;
    var pageRow = 10;
    var pageAll = parseInt(dataLength/pageRow)<dataLength/pageRow?parseInt(dataLength/pageRow+1):parseInt(dataLength/pageRow);
    function pageFresh() {
        tbody.innerHTML = null;
        ul.innerHTML = null;
        curPage = parseInt(curPage);
        var start = (curPage-1)*pageRow;
        var end = dataLength>curPage*pageRow?curPage*pageRow:dataLength;
        //表格

        for (let i = start;i < end; i ++) {
            var row = data[i];
            var tr = document.createElement("tr");
            Object.keys(row).forEach(function (key) {
                var td = document.createElement("td");
                td.innerHTML = row[key];
                tr.appendChild(td);
            })
            tbody.appendChild(tr);
        }
        //分页按钮

        var li_previous = document.createElement("li");
        var a_previous = document.createElement("a");
        a_previous.innerHTML = "上一页";
        a_previous.id = "上一页";
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
        a_next.innerHTML = "下一页";
        a_next.id = "下一页";
        li_next.appendChild(a_next);
        ul.appendChild(li_next);
        $("#"+id+"_ul li").attr("class","page-item");
        $("#"+id+"_ul a").attr("class","page-link");
        $("#"+id+"_ul a").attr("href","#");
        document.getElementById(id+curPage.toString()).parentElement.className = "page-item active";
        ul.onclick = function (e) {
            if (e.target.nodeName == "A"&&e.target.innerHTML !="...") {
                switch (e.target.innerHTML) {
                    case '上一页':
                        curPage = curPage>1?curPage-1:1;
                        break;
                    case '下一页':
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
    //排序

    // function clear_sel(doc){
    //      Object.keys(doc).forEach(function(index){
    //        sort_th[index].childNodes[1].className = "glyphicon glyphicon-sort";
    //      })
    // }
    // //判断是否为数值
    // function isNumber(val) {
    //     var val = val.replace(/&nbsp;/,"");
    //     var val = val.replace(/&nbsp;/,"");
    // var pattern = /^(\-|\+)?\d+(\.\d+)?$/;
    // return pattern.test(val)?true:false;
    // }
    // clear_sel(sort_th);
    // Object.keys(sort_th).forEach(function(index){
    //     sort_th[index].childNodes[1].onclick = function (e) {
    //         console.log(e.target.className);
    //         switch (e.target.className) {
    //             case 'glyphicon glyphicon-sort-by-attributes':
    //             function decendnot(x,y){
    //                 // if(isNumber(y[e.target.parentElement.cellIndex]+x[e.target.parentElement.cellIndex]))
    //                 //     return y[e.target.parentElement.cellIndex]-x[e.target.parentElement.cellIndex];
    //                 // else
    //                     return (y[e.target.parentElement.cellIndex]).localeCompare(x[e.target.parentElement.cellIndex]);
    //             }
    //             data = data.sort(decendnot);
    //             pageFresh();
    //             clear_sel(sort_th);
    //             e.target.className = 'glyphicon glyphicon-sort-by-attributes-alt';
    //             break;
    //             case 'glyphicon glyphicon-sort-by-attributes-alt':
    //             function ascendnot(x,y){
    //                 // if(isNumber(y[e.target.parentElement.cellIndex])+x[e.target.parentElement.cellIndex])
    //                 //     return x[e.target.parentElement.cellIndex]-y[e.target.parentElement.cellIndex];
    //                 // else
    //                     return (x[e.target.parentElement.cellIndex]).localeCompare(y[e.target.parentElement.cellIndex]);
    //             }
    //             data = data.sort(ascendnot);
    //             pageFresh();
    //             clear_sel(sort_th);
    //             e.target.className = 'glyphicon glyphicon-sort-by-attributes';
    //             break;
    //             default:
    //             function ascendnot(x,y){
    //                 // if(isNumber(y[e.target.parentElement.cellIndex])+x[e.target.parentElement.cellIndex])
    //                 //     return x[e.target.parentElement.cellIndex]-y[e.target.parentElement.cellIndex];
    //                 // else
    //                     return (x[e.target.parentElement.cellIndex]).localeCompare(y[e.target.parentElement.cellIndex]);
    //             }
    //             data = data.sort(ascendnot);
    //             pageFresh();
    //             clear_sel(sort_th);
    //             e.target.className = 'glyphicon glyphicon-sort-by-attributes';
    //             break;
    //         }
    //     }
    // });

}
