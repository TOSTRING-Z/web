from django.template import loader
from .models import mainRead,detailRead,tagClassRead,tagRead,commentIdRead,commenHuifuRead,owoSubmitRead
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index(request):
    return render(request, 'index.html')
def detail(request, id):
    return render(request, 'detail.html')
def about(request):
    return render(request, 'about.html')
def archives(request):
    return render(request, 'archives.html')
def goal(request):
    return render(request, 'goal.html')
def tags(request):
    return render(request, 'tags.html')
def tagSearch(request,tag):
    return render(request, 'search.html')
def json(request,index):
    result = mainRead(index=index)
    return JsonResponse(result, safe=False)
def detailJson(request,id):
    result = detailRead(id=id)
    return JsonResponse(result, safe=False)
def tagJson(request,tag,index):
    result = tagRead(tag=tag,index=index)
    return JsonResponse(result, safe=False)
def tagClass(request):
    result = tagClassRead()
    return JsonResponse(result, safe=False)
def commentId(request,id):
    result = commentIdRead(id=id)
    return JsonResponse(result, safe=False)
def commenHuifu(request):
    detail_id = request.GET['detail_id']
    result = commenHuifuRead(detail_id=detail_id)
    return JsonResponse(result, safe=False)
def owoSubmit(request):
    user_name = request.GET['user_name']
    email = request.GET['email']
    web_site = request.GET['web_site']
    target_user_id = request.GET['target_user_id']
    detail_id = request.GET['detail_id']
    content = request.GET['content']
    type = request.GET['type']
    owoSubmitRead(detail_id=detail_id,type=type,user_name=user_name,content=content,email=email,web_site=web_site,target_user_id=target_user_id)
    response = HttpResponse('ok')
    response.set_cookie('user_name', user_name, max_age=365*24*60*60)
    response.set_cookie('email', email, max_age=365*24*60*60)
    response.set_cookie('web_site', web_site, max_age=365*24*60*60)
    return response