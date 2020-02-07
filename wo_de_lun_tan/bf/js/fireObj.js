var fire = {
	aler:function(){alert("ok");},
	on:function (doc,e,fun){
		doc.addEventListener?doc.addEventListener(e,fun,false):doc.attachEvent("on"+e,fun);
	},
	un:function(doc,e,fun){
		doc.removeEventListener?doc.removeEventListener(e,fun,false):doc.detachEvent("on"+e,fun);
	},
	bind:function(foo,bin){
		return function(){
			foo.apply(bin,arguments);
		}
	},
	randN:function(minN,maxN){
		return Math.floor(Math.random() * (maxN - minN + 1)+minN);
	},
	randC:function(){
		var str = this.randN(0, 0xFFFFFF).toString(16);
		while (str.length < 6) str = "0" + str;
		return "#" + str;
		}
};
/****************/
function start(){
this.Manual = fire.bind(this.manual,this);
}
start.prototype = {
	sar:function(){
	fire.un(document,"click",this.Manual);
	fire.on(document,"click",this.Manual);
	},
	manual:function(event){
		event = event||window.event;
		this.create({x:event.pageX,y:event.pageY});
	},
	create:function(focu){
		//console.log(focu.x);
		//console.log(focu.y);
		var timer = null;
		var chips = new Array;
		var frag = document.createDocumentFragment();

		for(i = 0;i < 6;i ++){
			chips[i] = document.createElement("div");
			chips[i].speedX = fire.randN(-5,5);
			chips[i].speedY = fire.randN(-5,2);

			with(chips[i].style)
			{

				//console.log(event.scrollbars);
				top = focu.y + "px";
				left = focu.x + "px";
				width = "4px";
				height = "4px";
				zIndex = "30000";
				position = "absolute";
				overflow = "hidden";
				borderRadius = "4px";
				background = fire.randC();
			}
			frag.appendChild(chips[i]);
		}
		document.body.appendChild(frag);
		var j = 0;
		timer = setInterval(function(){

			for(i = 0; i < chips.length;i ++)
			{
					obj = chips[i];
					with(obj.style)
					{
					top = obj.offsetTop + obj.speedY + "px";
					left = obj.offsetLeft + obj.speedX + "px";
					opacity  = 1 - j;
					}
					//var N = (document.body.scrollTop)||(document.documentElement.scrollTop);
					//console.log("N:"+N+"  document.documentElement.scrollTop:"+document.documentElement.scrollTop+"    document.body.scrollTop:"+document.body.scrollTop+"   document.documentElement.clientHeight:"+document.documentElement.clientHeight+"   obj.offsetTop:"+obj.offsetTop);
					obj.speedY ++;
					(obj.style.opacity <= 0||obj.offsetTop <= 0 || obj.offsetLeft <= 0 ||obj.offsetTop > document.documentElement.clientHeight+((document.body.scrollTop)||(document.documentElement.scrollTop))|| obj.offsetLeft >= document.documentElement.clientWidth-5) && (document.body.removeChild(obj), chips.splice(i, 1))
					chips[0] || clearInterval(timer);
			}
			j += 0.2;

		},50);
	}
}
/****************/
function keyup(even){
	var end = even.selectionEnd;
	var beforeText = even.value.slice(0,end);
	var afterText =even.value.slice(end);
	var mir = "<div id='mir' style='position:absolute;visibility: hidden;white-space: nowrap' class='"+even.className+"'>"+beforeText+"<span id='cursor'>|</span>"+afterText+"</div>";
	even.insertAdjacentHTML("afterend",mir);
	var cursor = document.getElementById('cursor');
	var e = cursor.getBoundingClientRect();
	var s = even.getBoundingClientRect();
	left1 = e.left;
    e.left >= (s.left + s.width)&&(left1 = s.left + s.width);
    // console.log(s);
	// console.log(e);
	var timer = null;
	var chips = new Array;
	var frag = document.createDocumentFragment();

	for(i = 0;i < 5;i ++){
		chips[i] = document.createElement("div");
		chips[i].speedX = fire.randN(-5,5);
		chips[i].speedY = fire.randN(-5,2);
		with(chips[i].style)
		{

			top = e.top + ((document.documentElement.scrollTop)||(document.body.scrollTop)) + "px";
			left = left1 + "px";
			width = "3px";
			height = "3px";
			zIndex = "30000";
			position = "absolute";
			overflow = "hidden";
			borderRadius = "3px";
			background = fire.randC();
		}

		frag.appendChild(chips[i]);
	}
	document.body.appendChild(frag);
	var j = 0;
	timer = setInterval(function(){

		for(i = 0; i < chips.length;i ++)
		{
				obj = chips[i];
				with(obj.style)
				{
				top = obj.offsetTop + obj.speedY + "px";
				left = obj.offsetLeft + obj.speedX + "px";
				opacity  = 1 - j;
				}
				//console.log(obj);
				obj.speedY ++;
				(obj.style.opacity <= 0||obj.offsetTop <= 0 || obj.offsetLeft <= 0 || obj.offsetTop >= document.documentElement.clientHeight + ((document.documentElement.scrollTop)||(document.body.scrollTop)) || obj.offsetLeft >= document.documentElement.clientWidth-5) && (document.body.removeChild(obj), chips.splice(i, 1))
				!chips[0] && clearInterval(timer);
		}
		j += 0.2;

	},50);
	var mi = document.getElementById("mir");
	var pa = document.getElementById("search");
	pa.removeChild(mi);
}
/****************/
fire.on(window,"load",function(){
	var Start = new start();
	Start.sar();

	//fire.on(document,"click",Start.Manual);
	//console.log(Start.Manual);
	});