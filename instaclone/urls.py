"""instaclone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from django.views.static import serve
from django.conf.urls import url





from home import views as hm

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', hm.home, name='home'),
    path('discover/', hm.discover, name='discover'),
    
    
    path('login/', hm.login, name='login'),
    path('logout/',hm.logout, name='logout'),
    path('register/',hm.register, name='register'),
    path('mypr/', hm.mypr, name="myprofile"),
    path('up/',hm.uploadphoto),
    path('us/',hm.uploadstatus, name='us'),
    path('uv/',hm.uploadvideo),
    path('usp/<str:name>/',hm.userspecificprofile),
    path('editprofile/',hm.editprofile, name='editprofile'),
    path('delete/<int:id>/',hm.deletepost),
    path('editpost/<int:id>/',hm.editpost),
    path('editvideopost/<int:id>/',hm.editvideopost),
    path('addcomment/<int:id>/',hm.addcomment, name='addcomment'),
    path('deleteaccount/<str:name>/',hm.deleteaccount, name='deleteaccount'),
    path('newfeatures/', hm.newfeatures),
    path('updateprofilepicture/', hm.updateprofilepicture),

    path('allcomments/<int:id>/', hm.allcomments, name='allcomments'),
    path('allcomments1/<int:id>/', hm.allcomments1,),
    path('myprofiledeletecomment/<int:id>/', hm.myprofiledeletecomment),
    path('accounts/', include('django.contrib.auth.urls')),


    path('chat/<str:name>/', hm.chatbox, name='chat'),
    path('addmessage/', hm.addmessage),

    path('chathome/', hm.chathome, name='chathome'),

    path('deletemymessage/<int:id>/', hm.deletemymessage),

    path('chatinfo/', hm.chatinfo),

    path('addfollow/', hm.addfollow),
    path('addprivatefollow/', hm.addprivatefollow),
    path('deleteprivatefollow/', hm.deleteprivatefollow),
    path('unfollow/', hm.unfollow),
    path('unfollowfromprofile/<str:name>/', hm.unfollowfromprofile),
    path('viewfollowers/', hm.viewfollowers, name='viewfollowers'),
    path('viewfollowing/', hm.viewfollowing, name='viewfollowing'),
    path('chatsendimages/', hm.chatsendimages),

    path('changebackgroundimage/', hm.changebackgroundimage),

    path('addtoprivate/', hm.addtoprivate),
    path('unprivate/', hm.unprivate),
    path('notifications/',hm.notifications, name='notifications'),

    path('privaterequestfollow/', hm.requestprivatefollow),

    path('searchbox/', hm.searchbox, name='searchbox'),

    path('removetempnoti/', hm.removetempnoti),

    path('blockchatuser/', hm.blockchatuser),
    path('unblockchatuser/', hm.unblockchatuser),
    path('addlike/',hm.addlike),
    path('removelike/',hm.removelike),
    path('viewpost/<int:id>/',hm.viewpost),
     path('homeaddlike/',hm.homeaddlike),

     path('removelfc/', hm.removelfc),



     path('contactdeveloper/',hm.contactdeveloper),

     path('viewlikes/<int:id>/', hm.viewlikes),
     path('removefollowerfromprofile/<str:name>/', hm.removefollowerfromprofile),

     path('grouppage/<int:id>/', hm.grouppage),

     path('changegrouppicturepage/<int:id>/', hm.changegrouppicturepage),

     path('changegrouppicture/', hm.changegrouppicture),

     path('creategroup/', hm.creategroup),

     
   


    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

    path('groupchat/<int:id>/', hm.groupchat),
    path('groupsendmessages/', hm.groupsendmessages),
    path('addpeoplepage/<int:id>/', hm.addpeoplepage, name='addpeoplepage'),
    path('addmember/', hm.addmember, name='addmember'),




#serializer
    path('viewusers/',hm.Viewusers.as_view(), name='viewusers'),
    path('Viewcontactdeveloperrequest/', hm.Viewcontactdeveloperrequest.as_view()),
    path('auth/', include('rest_framework.urls')),
    
]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        )


     