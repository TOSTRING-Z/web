from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('archives/', views.archives, name='archives'),
    path('about/', views.about, name='about'),
    path('goal/', views.goal, name='goal'),
    path('tags/', views.tags, name='tags'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:index>/json/', views.json, name='json'),
    path('<int:id>/detail/', views.detailJson, name='detailJson'),
    path('<str:tag>/<int:index>/tag/', views.tagJson, name='tagJson'),
    path('<str:tag>/tag/', views.tagSearch, name='tagSearch'),
    path('tags/class/', views.tagClass, name='tagClass'),
    path('comment/<int:id>/', views.commentId, name='commentId'),
    path('comment/huifu/', views.commenHuifu, name='commenHuifu'),
    path('owoSubmit', views.owoSubmit, name='owoSubmit'),
]
