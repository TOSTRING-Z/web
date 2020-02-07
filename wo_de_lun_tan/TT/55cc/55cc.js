id = '';
$('.ff-vod-img-new > a').attr('href', function (i, d) {
    if(i==0)
        id += d.split('/')[2];
    else
        id += (',' + d.split('/')[2]);
});
id = '['+id+']';