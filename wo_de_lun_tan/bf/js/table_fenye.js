$("#dataTable tbody tr").find(":first").css("color","rgb(70,130,180)");
var shows = document.getElementsByClassName("xianshi");
//记录所有行数
var allrows = shows.length;
//记录每页显示行数,初始为10行
var pageShowRows = 10;
//记录当前是第几个页面
var curPage = 1;
//记录所有页面数
var num = allrows/pageShowRows;
if(num <= parseInt(num)) var allPage = parseInt(num);
else var allPage = parseInt(num)+1;
//界面刷新,分页功能
function reLoad()
	{
		var shows = document.getElementsByClassName("xianshi");
		//记录所有行数
		allrows = shows.length;
		$("#dataTable #allrows").html("<div class='col-xs-12 col-md-12'>Showing "+(pageShowRows*(curPage-1)+1)+" to "+((pageShowRows*curPage)>allrows?allrows:(pageShowRows*curPage))+" of "+allrows+" entries");
		//记录所有页面数
		num = allrows/pageShowRows;
		if(num <= parseInt(num)) allPage = parseInt(num);
		else allPage = parseInt(num)+1;
		//隐藏其余页面
		$("#dataTable tbody tr").hide();
		//显示当前页面
		for(i=pageShowRows*(curPage-1);i<pageShowRows*curPage;i++)
		{
			if(i<allrows)
			$("#dataTable tbody .xianshi")[i].style.display = "";
		}
		//页面选择键
		//开始
		if(curPage>2) var start = curPage-2;
		else if(curPage==2)var start = 1;
		else var start = curPage;
		//结束
		if(curPage<allPage-1) var end = curPage+2;
		else if(curPage==allPage-1) var end = allPage;
		else var end = allPage;
		$("#dataTable #pageSel").html("");
		$("#dataTable #pageSel").append("<li><a class='psel' id='Previous'>&laquo;</a></li>");
		for(var i=start;i<=end;i++)
		{
			$("#dataTable #pageSel").append("<li><a id='psela'>"+i+"</a></li>");
		}
		$("#dataTable #pageSel").append("<li><a class='psel' id='Next'>&raquo;</a></li>");
		$("#dataTable #pageSel").find("a:contains("+curPage+")").css("background-color","rgb(70,130,180)").css("color","#f0f0f0");
		//界面跳转
	    $("#dataTable tbody tr").find(":first").click(function(e) {
	        var url = $(e.target).text().trim();
	        var url = url.split("_");
	        $(location).attr("href","search/search_result_sample.php?sample_id="+url[0]+"_"+url[1]+"_"+url[2]);
	    });
}
reLoad();
$(document).ready(function(e) {
	//返回alldata
	$("#dataTable #allrows").click(function(e) {
		$("#dataTable input").val("");
		 var searchVal = $("#search input").val();
		$("#dataTable .yingchang").filter(":contains("+searchVal+")").attr("class","xianshi");
		$("#dataTable .screen").find("#click").each(function(index, element) {
			$("#dataTable .xianshi").filter(":not(:contains("+$(element).text()+"))").attr("class","yingchang");
		});
		vals = [];
		curPage = 1;
		reLoad();
    });
	//点击当前页面下选择按钮，选择页面,此处使用事件委托（添加的元素没有事件绑定）
	$("#dataTable #pageSel").click(function(e) {
		var e = event||window.event;
		if(e.target.id=="psela")
		curPage = parseInt($(e.target).text());//接收为字符！！！！不是数字
		reLoad();
	});
	//下拉每页显示数
	$("#dataTable select").change(function(e) {
        pageShowRows = $(e.target).val();
		curPage = 1;
		reLoad();
    });
	//当前页面数
    $("#dataTable #pageSel").click(function(e) {
    	var e = event||window.event;
		var target = e.target||e.srcElement
		if(target.className=="psel"){
        switch(target.id)
		{
			case 'Previous':
				curPage = 1;
				break;
			default:
				curPage = allPage;
		}
		reLoad();
	}
    });
	//搜索功能
	$("#dataTable #search input").keyup(function(e) {
        var searchVal = $("#dataTable #search input").val();
		$("#dataTable .yingchang").filter(":contains("+searchVal+")").attr("class","xianshi");
		$("#dataTable .screen").find("#click").each(function(index, element) {
			$("#dataTable .xianshi").filter(":not(:contains("+$(element).text()+"))").attr("class","yingchang");
		});
		$("#dataTable .xianshi").filter(":not(:contains("+searchVal+"))").attr("class","yingchang");
		shows = [];
		curPage = 1;
		reLoad();
	});
	//排序功能
    $("#dataTable thead td").click(function(event) {
		var event = event||window.event;
		if(event.target.localName=="a"&&event.currentTarget.localName=="td"){
		//判断是否为数值
		function isNumber(val) {
			var val = val.replace(/&nbsp;/,"");
			var val = val.replace(/&nbsp;/,"");
		var pattern = /^(\-|\+)?\d+(\.\d+)?$/;
		return pattern.test(val)?"is":"not";
		}
		var index = this.cellIndex;
		//sort
		var ifsort = $(this).attr("id")+isNumber($("#dataTable tbody tr")[0].cells[index].innerHTML);
		//判断排序
		switch(ifsort)
		{
			case "ascendnot"://升序notNumber
				$(this).attr("id","decend");
				function ascendnot(x,y){
				return (x.cells[index].innerText).localeCompare(y.cells[index].innerText);}
				this.tb = $("#dataTable tbody tr").sort(ascendnot);
				break;
			case "decendnot"://降序notNumber
				$(this).attr("id","ascend");
				function decendnot(x,y){
				return (y.cells[index].innerText).localeCompare(x.cells[index].innerText);}
				this.tb = $("#dataTable tbody tr").sort(decendnot);
				break;
			case "ascendis"://升序isNumber
				$(this).attr("id","decend");
				function ascendis(x,y){
				//parseInt();字符转数值
				x.cells[index].innerHTML = x.cells[index].innerHTML.replace(/&nbsp;/,"");
				x.cells[index].innerHTML = x.cells[index].innerHTML.replace(/&nbsp;/,"");
				y.cells[index].innerHTML = y.cells[index].innerHTML.replace(/&nbsp;/,"");
				y.cells[index].innerHTML = y.cells[index].innerHTML.replace(/&nbsp;/,"");
				return x.cells[index].innerHTML - y.cells[index].innerHTML;}
				this.tb = $("#dataTable tbody tr").sort(ascendis);
				break;
			case "decendis"://降序isNumber
				$(this).attr("id","ascend");
				function decendis(x,y){
				//parseInt();字符转数值
				x.cells[index].innerHTML = x.cells[index].innerHTML.replace(/&nbsp;/,"");
				x.cells[index].innerHTML = x.cells[index].innerHTML.replace(/&nbsp;/,"");
				y.cells[index].innerHTML = y.cells[index].innerHTML.replace(/&nbsp;/,"");
				y.cells[index].innerHTML = y.cells[index].innerHTML.replace(/&nbsp;/,"");
				return y.cells[index].innerHTML - x.cells[index].innerHTML;}
				this.tb = $("#dataTable tbody tr").sort(decendis);
				break;
		}
		//console.log(this.tb);
		$("#dataTable tbody").html(this.tb);
		vals = [];
		curPage = 1;
		reLoad();
		}
    });
});
//调整列宽
//固定第一列
var fun = {
	on:function(doc,type,handler){
		return doc.addEventListener?doc.addEventListener(type,handler,false):doc.attachEvent("on" + type,handler);
		},
	un:function(doc,type,handler){
		return doc.removeEventListener?doc.removeEventListener(type,handler,false):doc.detachEvent("on" + type,handler);
		},
	over:function(doc){
		return function(){
				if(event.offsetX > doc.offsetWidth-10){
				fun.un(doc,"mousedown",handler_mousedown);
				doc.style.cursor = 'col-resize'; 
				handler_mousedown= fun.down(doc);
				fun.on(doc,"mousedown",handler_mousedown);
				}
				else if(event.offsetX < doc.offsetWidth-20){
				doc.style.cursor = 'pointer';
				}
			}
		},
	 clearEvent:function(doc){
	 	return function(){
				fun.un(doc,"mousemove",handler_mousemove);
				fun.un(document,"mouseup",handler_mouseup);
	 		}	
		},
	 move:function(doc){
	 	return function(){
		 		//if(event.offsetX+20 > doc.offsetWidth-40)
				doc.width = event.offsetX+20;
		 	}
		},
	 down:function(doc){
		return	function(){
			fun.un(doc,"mousemove",handler_mousemove);
			fun.un(document,"mouseup",handler_mouseup);
			handler_mouseup = fun.clearEvent(doc);
			handler_mousemove = fun.move(doc);
			fun.on(doc,"mousemove",handler_mousemove);
			fun.on(document,"mouseup",handler_mouseup);
			}
		}
	}
	var handler_mouseover = null;
	var handler_mousemove = null;
	var handler_mousedown = null;
	var handler_mouseup = null;
	var tab = document.getElementById("tb_1");
	for(var i = 0;i < tab.rows[0].cells.length-1;i ++){
		var doc = tab.rows[0].cells[i];
		if(i<tab.rows[0].cells.length-1)doc.width = "150px";
		handler_mouseover = fun.over(doc);
		fun.on(doc,"mouseover",handler_mouseover);
		}
//悬停提示
var fun1 = {
      on:function(doc,e,funs){
        doc.addEventListener?doc.addEventListener(e,funs,false):doc.attendEvent("on"+e,funs);
        },
      un:function(doc,e,funs){
        doc.removeEventListener?doc.removeEventListener(e,funs,false):doc.detachEvent("on"+e,funs);
        },
      Show:function(){
          var event = event||window.event;
          if(event.target.localName=="td"){
           floatShow.style.backgroundColor="#555";
           floatShow.style.color="#fff";
           floatShow.style.opacity=0.9;
           floatShow.style.left=event.pageX+10+"px";
           floatShow.style.top=event.pageY+15+"px";
           floatShow.innerHTML=event.target.innerText;
          }
        },
    Hide:function(){
        floatShow.style.opacity=0;
      }
      };
$("<div>",{
      "id":"floatShow",
      "style":"border:solid 1px #F0F0F0;position:absolute;left:0;top:0;align:center;padding:5px;opacity:0"
      }).appendTo("body");
var tables = document.getElementsByTagName("table")[0];
//console.log(tables);
var floatShow=document.getElementById("floatShow");
fun1.on(tables,"mouseover",fun1.Show);
fun1.on(tables,"mousemove",fun1.Show);
fun1.on(tables,"mouseout",fun1.Hide);
	