from django.urls import path  # Importe la fonction path(url,view.functionName)
# Importe la fonction url(url,view.functionName)
from django.conf.urls import url, include
from django.conf import settings  # Recupère setting.py
from . import views  # Recupère les views

app_name = 'home'  # Donne le nom de l'app


urlpatterns = [

    # path('[insérer l'url après le domaine]',views.[insérer fonction depuis view.py],[peut insérer un nom mais facultatif])


    path('', views.gotoIndexNoSort),
    path('index', views.gotoIndexNoSort),
    path('index/<str:sortBy>', views.gotoIndex),
    path('thread-<int:thread_id_gotten>', views.gotoThread),
    path('new_thread', views.gotoNewThread, name='gotoNewThread'),
    path('auth', views.gotoAuth),
    path('profil/<str:nameOfUser>', views.gotoProfil),
    path('auth/complete/google-oauth2', views.gotoLogged),
    path('create_post', views.createPost),
    path('modify_thread', views.modifyThread),
    path('modify_post', views.modifyPost),
    path('modify_childpost', views.modifyChildPost),
    path('thread_modified', views.threadModified),
    path('post_modified', views.postModified),
    path('childpost_modified', views.childPostModified),
    url(r'^logout/$', views.logout, name='logout'),

    # Ajax redirection url
    path('ajax/add_childpost/', views.addChildPost, name="addChildPost"),
    path('ajax/pin_post/', views.pinPost),
    path('ajax/delete_thread/', views.deleteThread),
    path('ajax/delete_post/', views.deletePost),
    path('ajax/delete_childpost/', views.deleteChildPost),
    path('ajax/lock_thread/<str:lock>', views.lockThread)
    # path('ajax/add_post/',views.addPost,name="addPost"),

]
