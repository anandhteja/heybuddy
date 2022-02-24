from logging.config import dictConfig
from venv import create
from webbrowser import get
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import Contactdeveloper, Post, Profile,Creategroup,Grouppeople,Groupsendmessages,Verifiedaccounts, Comment, Chat, Follow, Chatbackground, Privateaccount, Privatefollow,Likefollowcommentnoti, Temporarynotification, Chatblock,Likes
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from home.forms import Editprofile,Editpost, Editvideopost
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from home.serializers import Userserializer, Contactdeveloperserializer
from rest_framework.generics import ListAPIView

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from django.test import TestCase
from rest_framework.generics import ListAPIView


from django.contrib import messages











# Create your views here.
@login_required(login_url='login')
def home(request):
    
    
    
    for k,v in request.session.items():
        if k in 'username':
            usern=User.objects.get(username=v)
            pp=Profile.objects.all()
            p=Profile.objects.get(username=v)
            c=Comment.objects.all().order_by('-uploaded_on')[:6]
            user=list(User.objects.all().filter(username=v).values_list('username', flat=True))
              
            po=Post.objects.all().order_by('-uploaded_on')
            f=list(Follow.objects.all().filter(follower=v).values_list('following',flat=True))
            
            private=list(Privateaccount.objects.all().values_list('username',flat=True))
            likes=Likes.objects.all()
            verified=list(Verifiedaccounts.objects.all().values_list('username', flat=True))



            
            dict={'usern':usern,'post':po,'pp':pp,'co':c,'p':p, 'f':f, 'private':private,'user':user, 'verified':verified,'likes':likes}
            
            return render(request,'home.html',dict)



@login_required(login_url='login')
def discover(request):
    
    
    
    for k,v in request.session.items():
        if k in 'username':
            usern=User.objects.get(username=v)
            pp=Profile.objects.all()
            p=Profile.objects.get(username=v)
            c=Comment.objects.all().order_by('-uploaded_on')[:6]
            usern=usern
           
              
            po=Post.objects.all().order_by('-uploaded_on')
            f=list(Follow.objects.filter(follower=v).values_list('following',flat=True))
            

            private=list(Privateaccount.objects.all().values_list('username',flat=True))
            verified=list(Verifiedaccounts.objects.all().values_list('username', flat=True))

            
            dict={'usern':usern,'post':po,'pp':pp,'co':c,'p':p, 'f':f, 'private':private,'verified':verified}
            
            return render(request,'discover.html',dict)










def login(request):
    if request.method=='POST':
        u=request.POST['username']
        p=request.POST['password']
        user=auth.authenticate(username=u, password=p)
        if user is not None:
            auth.login(request, user)
            request.session['username']=u

            return redirect('home')
        else:
            messages.success(request,"invalid credentials or Account doesn't exists")
            return redirect('home')
            
    return render(request,'authentication/login.html')




def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        e=request.POST['email']
        f=request.POST['fullname']
        
        u=request.POST['username']
        p1=request.POST['password1']
        p2=request.POST['password2']
            
        ph=request.FILES['profilephoto']
        cbi=request.FILES['backgroundimage']
        d=request.POST['description']
        if User.objects.all().filter(username=u):
            messages.error(request,'username already exists')
        
        elif Profile.objects.all().filter(username=u):
            messages.error(request,'username already exists')
        elif User.objects.all().filter(email=e):
            messages.error(request,'email already exists')

        elif p1==p2:
            pho=Profile.objects.create(username=u, profilephoto=ph,description=d)
            user=User.objects.create_user(email=e,first_name=f,username=u, password=p1)
            background=Chatbackground.objects.create(username=u,image=cbi)
            
            user.save()
            pho.save()
            background.save()
            messages.success(request,'Your account has been created successfully')
            return redirect('login')
           
        else:
           return HttpResponse("password doesn't match")
            
            



                
                


        
    return render(request, 'authentication/registration.html')



@login_required(login_url='login')

def mypr(request):
     
    for k,v in request.session.items():
        if k in 'username':
            usern=User.objects.get(username=v)
            pp=Profile.objects.get(username=v)

            
            username=usern
           
            count=Post.objects.filter(username=usern).count()
            po=Post.objects.filter(username=v).order_by('-uploaded_on')
            c=Comment.objects.all().order_by('-uploaded_on')[:5]
            followercount=Follow.objects.filter(following=v).count()
            followingcount=Follow.objects.filter(follower=v).count()
            verified=list(Verifiedaccounts.objects.all().values_list('username', flat=True))


            
            dict={'usern':usern,'post':po,'pp':pp,'co':c,'count':count, 'followercount':followercount,'followingcount':followingcount,'verified':verified}
            return render(request,'myprofile.html',dict)


@login_required(login_url='login')
def uploadphoto(request):
    
    if request.method=='POST':
        for k,v in request.session.items():
            if k in 'username':
                u=v
               
                p=request.FILES['photos']
                d=request.POST['description']

                            
                po=Post(username=u,photos=p,description=d)
                po.save()
                messages.success(request,'Photo uploaded successfully')
                return redirect('home')
    
    return render(request,'upload/uploadphoto.html')


@login_required(login_url='login')
def uploadstatus(request):
    
    if request.method=='POST':
        for k,v in request.session.items():
            if k in 'username':
                u=v
               
                s=request.POST['status']

                if len(s) > 0:

                    po=Post(username=u,status=s)
                    po.save()
                    messages.success(request,'Status uploaded successfully')

                    return redirect('home')
                else:
                    messages.info(request,"Status shouldn't be empty")
                    return redirect('us')
    
    return render(request,'upload/uploadstatus.html')







@login_required(login_url='login')

def userspecificprofile(request,name):
    for k,v in request.session.items():
        if k in 'username':
            
            opp=Profile.objects.get(username=v)
    
  
            usern=User.objects.get(username=name)
            pp=Profile.objects.get(username=name)

                    
            username=v
                
                    
            po=Post.objects.filter(username=usern).order_by('-uploaded_on')
            count=Post.objects.filter(username=usern).count()
            private=list(Privateaccount.objects.all().values_list('username',flat=True))
            f=list(Follow.objects.all().filter(follower=v, following=name).values_list('following',flat=True))
            verified=list(Verifiedaccounts.objects.all().values_list('username', flat=True))
            

            req=Privatefollow.objects.all()
            try:
                follow=Follow.objects.get(follower=v,following=name)
            except:
                follow=Follow.objects.filter(follower=v,following=name)

            
            

                    
            dict={'usern':usern,'post':po,'pp':pp,'opp':opp, 'count':count, 'private':private,'username':username,'req':req,'follow':follow, 'f':f, 'verified':verified}
            return render(request,'userspecificprofile.html',dict)


@login_required(login_url='login')

def editprofile(request):
    for k,v in request.session.items():
        if k in 'username':
            
    
            u=v 
            pp=Profile.objects.get(username=v)
            form=Editprofile(instance=pp)
            private=list(Privateaccount.objects.all().values_list('username',flat=True))
            dict={'form':form,'username':u, 'private':private}
            if request.method == 'POST':
                
                d=request.POST['description']
                userinput=Profile.objects.filter(username=v).update(description=d)
                
                messages.success(request,'Your profile description has been updated successfully')
                    

                    

                  

                return redirect('myprofile')
        
            return render(request, 'edit/editprofile.html',dict)



@login_required(login_url='login')

def deletepost(request,id):
    p=Post.objects.get(id=id)
    co=Comment.objects.filter(postid=id)
    p.delete()
    co.delete()
    messages.success(request,'post removed successfully')
    return redirect('home')






@login_required(login_url='login')
def editpost(request, id):
    s=Post.objects.get(id=id)
    form=Editpost(instance=s)
    dict={'form':form}
    if request.method=="POST":
        userinput=Editpost(request.POST, instance=s)
        if userinput.is_valid():
            userinput.save()
            return redirect('home')

    return render(request,'edit/editpost.html',dict)



@login_required(login_url='login')

def addcomment(request,id):
    if request.method == 'POST':
        for k,v in request.session.items():
            if k in 'username':
                p=request.POST['postid']
                c=request.POST['comment']
                u=request.POST['post_user']
                username=v
                userinput=Comment.objects.create(username=v,postid=p,comment=c)
                lfc=Likefollowcommentnoti(postid=p,username=u, commented_by=v, comment=c)
                lfc.save()
                userinput.save()
                return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def deleteaccount(request, name):
    u=User.objects.get(username=name)
    p=Profile.objects.get(username=name)
    po=Post.objects.filter(username=name)
    co=Comment.objects.filter(username=name)
    ch=Chat.objects.filter(sender=name)
    ch1=Chat.objects.filter(receiver=name)
    cbi=Chatbackground.objects.all().filter(username=name)
    u.delete()
    p.delete()
    po.delete()
    co.delete()
    ch.delete()
    ch1.delete()
    cbi.delete()
    return HttpResponse('account deleted succesfully')


@login_required(login_url='login')
def newfeatures(request):
    for k,v in request.session.items():
        if k in 'username':
            usern=v
            dict={'usern':usern}
    return render(request,'newfeatures.html',dict)



class Viewusers(ListAPIView):
    queryset=User.objects.all()
    serializer_class=Userserializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAdminUser]



@login_required(login_url='login')
def updateprofilepicture(request):
    for k,v in request.session.items():
            if k in 'username':
                
                if request.method=='POST':
                    ph= Profile.objects.get(username=v)
                   
                    p=request.FILES.get('profilephoto')
                    d='Changed profilepicture'
                    ph.profilephoto=p
                    ph.save()
                    messages.success(request,'Profile picture has been updated successfully')
                
                    return redirect('myprofile')



                    
                        
                        
                        
                       
                    
    
   
    

    return render(request,'edit/updateprofilepicture.html')





@login_required(login_url='login')

def allcomments(request, id):
    co=Comment.objects.filter(postid=id).order_by('-uploaded_on')
    dict={'co':co}
    return render(request, 'allcomments.html',dict)



@login_required(login_url='login')

def myprofiledeletecomment(request,id):
    co=Comment.objects.filter(id=id)
    co.delete()
    return HttpResponse('comment deleted successfully')



@login_required(login_url='login')

def allcomments1(request,id):
    for k,v in request.session.items():
            if k in 'username':
                usern=v
                co=Comment.objects.filter(postid=id).order_by('-uploaded_on')
                dict={'co':co,'usern':usern}
    return render(request, 'allcomments1.html',dict)



@login_required(login_url='login')
def uploadvideo(request):
    
    if request.method=='POST':
        for k,v in request.session.items():
            if k in 'username':
                u=v
               
                v=request.FILES['videos']
                d=request.POST['videodescription']

                            
                po=Post(username=u,videos=v,video_description=d)
                po.save()
                messages.success(request,'Video uploaded successfully')

                return redirect('home')
    
    return render(request,'upload/uploadvideo.html')






@login_required(login_url='login')
def editvideopost(request, id):
    s=Post.objects.get(id=id)
    form=Editvideopost(instance=s)
    dict={'form':form}
    if request.method=="POST":
        userinput=Editvideopost(request.POST, instance=s)
        if userinput.is_valid():
            userinput.save()
            return HttpResponse('saved successfully')

    return render(request,'edit/editvideopost.html',dict)




@login_required(login_url='login')
def chatbox(request, name):
    for k,v in request.session.items():
            if k in 'username':
                usern=v
                unique=v+name
                unique1=name+v
                chat=Chat.objects.filter(unique=unique).order_by('-id') | Chat.objects.filter(unique=unique1).order_by('-id')
                sender=User.objects.get(username=v)
                receiver=User.objects.get(username=name)
                background=Chatbackground.objects.get(username=v)
                block=list(Chatblock.objects.all().filter(blocked_by=v, blocked_user=name).values_list('blocked_user', flat=True))
                block_by=list(Chatblock.objects.all().filter(blocked_user=v, blocked_by=name).values_list('blocked_user', flat=True))



                dict={'chat':chat, 'user':sender, 'receiver': receiver, 'usern':usern,'background':background, 'block':block, 'block_by':block_by}
                return render(request, 'chatpage.html', dict)




@login_required(login_url='login')
def addmessage(request):
    for k,v in request.session.items():
            if k in 'username':
                if request.method == 'POST':
                    sender=v
                    receiver=request.POST['receiver']
                    
                    message=request.POST['message']
                    if len(message)==0:
                        messages.info(request,"Can't send empty message")
                        return redirect(request.META['HTTP_REFERER'])
                    else:
                        unique=v+receiver
                        userinput=Chat(sender=sender, receiver=receiver, message=message, unique=unique)
                        tempnoti=Temporarynotification(sender=sender, receiver=receiver, message=message)
                        userinput.save()
                        tempnoti.save()

                        return redirect(request.META['HTTP_REFERER']) 



@login_required(login_url='login')
def chathome(request):
    for k,v in request.session.items():
            if k in 'username':
                chat=Chat.objects.filter(sender=v).values('receiver').distinct
                
                groups=Creategroup.objects.filter(created_by=v)
                groups1=Grouppeople.objects.filter(username=v)

                dict={'chat':chat, 'groups':groups, 'groups1':groups1}

    return render(request, 'chathome.html',dict)




@login_required(login_url='login')
def deletemymessage(request, id):
    d=Chat.objects.get(id=id)
    d.delete()
    return redirect(request.META['HTTP_REFERER'])
    


@login_required(login_url='login')
def chatinfo(request):
    return render(request, 'chatinfo.html')

@login_required(login_url='login')
def addfollow(request):
    for k,v in request.session.items():
            if k in 'username':
                follower=v
                following=request.POST['following']
                f=Follow(following=following, follower=follower)
                lfc=Likefollowcommentnoti(username=following,followed_by=v)
                f.save()
                lfc.save()
                messages.success(request,'Following')
                return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def unfollow(request):
    for k,v in request.session.items():
            if k in 'username':
                follower=v
                following=request.POST['following']
                f=Follow.objects.filter(follower=follower,following=following)
                f.delete()
                return redirect(request.META['HTTP_REFERER'])
@login_required(login_url='login')
def viewfollowers(request):
    for k,v in request.session.items():
            if k in 'username':
                f=Follow.objects.filter(following=v)
                dict={'fo':f}
                return render(request, 'follow/followers.html', dict)


@login_required(login_url='login')
def viewfollowing(request):
    for k,v in request.session.items():
            if k in 'username':
                f=Follow.objects.filter(follower=v)                
                dict={'fo':f}
                return render(request, 'follow/following.html', dict)

@login_required(login_url='login')
def unfollowfromprofile(request, name):
    for k,v in request.session.items():
            if k in 'username':
                follower=v
                following=name
                f=Follow.objects.filter(follower=follower,following=following)
                f.delete()
                return redirect('viewfollowing')



def removefollowerfromprofile(request, name):
     for k,v in request.session.items():
            if k in 'username':
                follower=name
                following=v
                f=Follow.objects.filter(follower=follower,following=following)
                f.delete()

                return redirect('viewfollowers')

@login_required(login_url='login')
def chatsendimages(request):
    for k,v in request.session.items():
            if k in 'username':
                if request.method == 'POST':
                    sender=v
                    n='sent an image'
                    receiver=request.POST['receiver']
                    chatimage=request.FILES['image']
                    unique=v+receiver
                    userinput=Chat(sender=sender, receiver=receiver,chat_photos=chatimage , unique=unique)
                    tempnoti=Temporarynotification(sender=sender, receiver=receiver,chat_photos=n)
                    userinput.save()
                    tempnoti.save()
                    return redirect(request.META['HTTP_REFERER'])



def changebackgroundimage(request):
    for k,v in request.session.items():
            if k in 'username':
                usern=v
                background=Chatbackground.objects.get(username=v)
                dict={'background':background,'usern':usern}
                if request.method == 'POST':
                    cbi=request.FILES['backgroundimage']
                    background.image=cbi
                    background.save()
                    messages.success(request,'Changed chat background successfully')
                    return redirect('chathome')
                return render(request,'backgroundimage/changebackgroundimage.html', dict)


def addtoprivate(request):
    for k,v in request.session.items():
            if k in 'username':
                p=Privateaccount(username=v)
                p.save()
                messages.success(request,'Your account is now private')
                return redirect('editprofile')



def unprivate(request):
    for k,v in request.session.items():
            if k in 'username':
                p=Privateaccount.objects.get(username=v)
                p.delete()
                messages.success(request,'Your account is now open')
                return redirect('editprofile')



def notifications(request):
    for k,v in request.session.items():
            if k in 'username':
                
                r=Privatefollow.objects.all()   
                n=Temporarynotification.objects.all().filter(receiver=v).order_by('-uploaded_on')[:10]
                lfc=Likefollowcommentnoti.objects.all().filter(username=v).order_by('-uploaded_on')
                usern=v
                dict={'r':r,'usern':usern, 'noti':n, 'lfc':lfc}


    return render(request, 'notifications.html',dict)




@login_required(login_url='login')
def addprivatefollow(request):
    for k,v in request.session.items():
            if k in 'username':
                following=v
                follower=request.POST['follower']
                f=Follow(following=following, follower=follower)
                d=Privatefollow.objects.get(requester=follower, requesting=v)
                f.save()
                d.delete()
                messages.success(request,'Accepted request successfully')
                return  redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def deleteprivatefollow(request):
    for k,v in request.session.items():
            if k in 'username':
                following=v
                follower=request.POST['follower']
                
                d=Privatefollow.objects.get(requester=follower, requesting=v)
                
                d.delete()
                messages.success(request,'Deleted request successfully')
                return redirect(request.META['HTTP_REFERER'])


def requestprivatefollow(request):
    for k,v in request.session.items():
            if k in 'username':
                requester=request.POST['requester']
                requesting=request.POST['requesting']
                p=Privatefollow(requester=requester, requesting=requesting)
                if Privatefollow.objects.filter(requester=v, requesting=requesting):
                    messages.success(request,"Request already sent, wait for the other person to respond")
                    return redirect(request.META['HTTP_REFERER'])
                else:
                    
                    p.save()
                    messages.success(request,"Request sent successfully")

                    return redirect(request.META['HTTP_REFERER'])

def searchbox(request):
    if request.method == 'GET':
        username=request.GET['username']
        user=User.objects.all().filter(username__icontains=username)
        tried=username
        dict={'user':user, 'tried':tried}


    return render(request,'searchbox.html',dict)    

    
def removetempnoti(request):
      for k,v in request.session.items():
            if k in 'username':
                d=Temporarynotification.objects.all().filter(receiver=v)
                d.delete()
                messages.success(request,"cleared")
                return redirect('notifications')


def blockchatuser(request):
    if request.method == 'POST':
        blocked_user=request.POST['blocked_user']
        blocked_by=request.POST['blocked_by']
        b=Chatblock(blocked_user=blocked_user, blocked_by=blocked_by)
        b.save()
        messages.success(request,'user blocked')
        return redirect(request.META['HTTP_REFERER'])


def unblockchatuser(request):
    if request.method == 'POST':
        blocked_user=request.POST['blocked_user']
        blocked_by=request.POST['blocked_by']
        b=Chatblock.objects.all().filter(blocked_user=blocked_user, blocked_by=blocked_by)
        b.delete()
        messages.success(request,'user unblocked')
        return redirect(request.META['HTTP_REFERER'])

def addlike(request):
    if request.method == 'POST':
        postid=request.POST['postid']
        liked_by=request.POST['liked_by']
        liked_user=request.POST['liked_user']
        l=Likes.objects.create(postid=postid,liked_by=liked_by)
        lfc=Likefollowcommentnoti(postid=postid,username=liked_user, liked_by=liked_by)
        lfc.save()
        
        l.save()
        messages.success(request,'liked sucessfully')
        return redirect(request.META['HTTP_REFERER'])

def viewpost(request, id):
     
    for k,v in request.session.items():
        if k in 'username':
            po=Post.objects.get(id=id)
            c=Comment.objects.all().order_by('-uploaded_on')[:6]
            f=list(Follow.objects.all().filter(follower=v).values_list('following',flat=True))
            l=Likes.objects.all().filter(liked_by=v, postid=id)
            pp=Profile.objects.all()
            likescount=Likes.objects.all().filter(postid=id).count()
            verified=list(Verifiedaccounts.objects.all().values_list('username', flat=True))
            
            
            usern=User.objects.get(username=v)
            dict={'po':po,'co':c,'f':f, 'usern': usern, 'l':l, 'pp':pp, 'likescount':likescount,'verified':verified}
            return render(request,'viewpost.html',dict)
 
def removelike(request):
        if request.method == 'POST':
            postid=request.POST['postid']
            liked_by=request.POST['liked_by']
            l=Likes.objects.get(postid=postid,liked_by=liked_by)
            
            l.delete()
            messages.success(request,"like removed successfully")
            return redirect(request.META['HTTP_REFERER'])


def homeaddlike(request):
    if request.method == 'POST':
        postid=request.POST['postid']
        liked_by=request.POST['liked_by']
        liked_user=request.POST['liked_user']
        if Likes.objects.all().filter(postid=postid,liked_by=liked_by):
            return HttpResponse('<h1> you already liked this post</h1>')
        else:
            
            l=Likes.objects.create(postid=postid,liked_by=liked_by)
            lfc=Likefollowcommentnoti(postid=postid,username=liked_user, liked_by=liked_by)
            lfc.save()
        
            l.save()
            return HttpResponse('<h1> You successfully liked this post </h1>')

def removelfc(request):
    d=Likefollowcommentnoti.objects.all()
    d.delete()
    messages.success(request,"cleared")
    return redirect('notifications')


def deleteconfirmation(request):
    for k,v in request.session.items():
            if k in 'username':
                username=v
                dict={'username':username}

    return render(request, 'deleteconfirmation.html',dict) 



def contactdeveloper(request):
    for k,v in request.session.items():
            if k in 'username':
                username=v
                dict={'username':username}
                if request.method == 'POST':
                    name=request.POST['name']
                    issue=request.POST['issue']
                    photos=request.FILES['photos']
                    email=request.POST['email']
                    c=Contactdeveloper(username=username, name=name, issue=issue,photos=photos, email=email)
                    c.save()
                    messages.success(request,'request has been sent to the developer, you will be contacted at the earliest possible')
                    return redirect('myprofile')
                    
    return render(request, 'contactdeveloper.html', dict)

class Viewcontactdeveloperrequest(ListAPIView):
    queryset=Contactdeveloper.objects.all()
    serializer_class=Contactdeveloperserializer
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAdminUser]



def viewlikes(request,id):
    likes=Likes.objects.all().filter(postid=id)
    dict={'likes':likes}
    return render(request, 'viewlikes.html', dict)




def groupchat(request, id):
    for k,v in request.session.items():
        if k in 'username':
            username=v

            people=Grouppeople.objects.all().filter(group_id=id).values_list('username', flat=True)
            people1=Creategroup.objects.all().filter(id=id).values_list('created_by', flat=True)
            if username in people or username in people1:


                c=Creategroup.objects.get(id=id)
                m=Groupsendmessages.objects.filter(group_id=id).order_by('-sent_on')
                background=Chatbackground.objects.get(username=v)
                dict={'c':c, 'username':username, 'm':m, 'background':background}
                return render(request, 'groupchat.html', dict)
            else:
                messages.info(request, 'You are not a member of this group')
                return redirect('chathome')


def groupsendmessages(request):
    if request.method == 'POST':
        group_id=request.POST['group_id']
        sender=request.POST['sender']
        message=request.POST['message']
        if len(message) == 0:
            messages.info(request,"Can't send empty messages")
            return redirect(request.META['HTTP_REFERER']) 
        else:
            g=Groupsendmessages(group_id=group_id, sender=sender, message=message)
            g.save()
            return redirect(request.META['HTTP_REFERER']) 







def addpeoplepage(request, id):
    for k,v in request.session.items():
            if k in 'username':
                f=Follow.objects.all().filter(follower=v)
                group_id=Creategroup.objects.get(id=id)
                
                people=list(Creategroup.objects.all().filter(id=id).values_list('created_by', flat=True))
                    
                
                people1=list(Grouppeople.objects.filter(group_id=id).values_list('username', flat=True))

                   
                dict={'f':f, 'group_id':group_id, 'people':people, 'people1':people1}

    
    return render(request,'addgrouppeople.html', dict)

def addmember(request):
   
    if request.method == 'POST':
        group_id=request.POST['group_id']
        username_1=request.POST['username']
        group_name=request.POST['group_name']
        for k,v in request.session.items():
            if k in 'username':
                username=v

                people=Grouppeople.objects.all().filter(group_id=group_id).values_list('username', flat=True)
                people1=Creategroup.objects.all().filter(id=group_id).values_list('created_by', flat=True)
                if username in people or username in people1:
                    user_input=Grouppeople(group_id=group_id, username=username_1, group_name=group_name)
                    gsm=Groupsendmessages(added_left=1,group_id=group_id, sender=username_1)
                    user_input.save()
                    gsm.save()
                    messages.info(request, 'Member added successfully')
                    return redirect('chathome')
                else:
                    messages.info(request, 'You are not a member of this group')
                    return redirect('chathome')
                
def grouppage(request, id):
    for k,v in request.session.items():
            if k in 'username':
                username=v

                people=list(Grouppeople.objects.all().filter(group_id=id).values_list('username', flat=True))
                people1=list(Creategroup.objects.all().filter(id=id).values_list('created_by', flat=True))
                if username in people or username in people1:
                    group=Creategroup.objects.get(id=id)
                    members=Grouppeople.objects.all().filter(group_id=id)
                    members1=Creategroup.objects.get(id=id)
                    dict={'group':group, 'members':members, 'members1':members1, 'login_user':username}
                    return render(request, 'grouppage.html', dict)


def changegrouppicturepage(request, id):
    for k,v in request.session.items():
            if k in 'username':
                username=v

                people=list(Grouppeople.objects.all().filter(group_id=id).values_list('username', flat=True))
                people1=list(Creategroup.objects.all().filter(id=id).values_list('created_by', flat=True))
                if username in people or username in people1:
                    id=id
                    dict={'id':id}
                    return render(request, 'changegrouppicturepage.html', dict)

def changegrouppicture(request):
    if request.method == 'POST':
        group_photo=request.FILES['group_photo']
        id=request.POST['id']
        object=Creategroup.objects.get(id=id)
        object.group_photo=group_photo
        object.save()
        messages.info(request, 'Group picture changed successfully')
        return redirect('chathome')

def creategroup(request):
    for k,v in request.session.items():
            if k in 'username':
                if request.method == 'POST':
                    group_name=request.POST['group_name']
                    group_photo=request.FILES['group_photo']
                    group_description=request.POST['group_description']
                    created_by=v
                    userinput=Creategroup(group_name=group_name, group_description=group_description, group_photo=group_photo, created_by=created_by)
                    userinput.save()
                    messages.info(request, 'Group created successfully')
                    return redirect('chathome')

    return render(request, 'creategroup.html')
                    
def deletegroup(request, id):
    for k,v in request.session.items():
            if k in 'username':
                group=Creategroup.objects.get(id=id)
                if group.created_by == v:
                    g=Creategroup.objects.get(id=id)
                    gp=Grouppeople.objects.all().filter(group_id=id)
                    gsp=Groupsendmessages.objects.all().filter(group_id=id)
                    g.delete()
                    gp.delete()
                    gsp.delete()
                    messages.info(request, 'Group deleted successfully')
                    return redirect('chathome')
                else:
                    messages.info(request, "you don't have access")
                    return redirect('chathome')

def leavegroup(request, id):
    for k,v in request.session.items():
            if k in 'username':
                group=Creategroup.objects.get(id=id)
                if group.created_by == v:
                    messages.info(request, 'Error! Only group members able to leave the group not the admin')
                    return redirect('chathome')
                else:

                    gp=Grouppeople.objects.all().filter(group_id=id, username=v)
                    gsp=Groupsendmessages(added_left=0, group_id=id, sender=v)
                    gp.delete()
                    gsp.save()
                    messages.info(request, 'You left the group successfully')
                    return redirect('chathome')


def removemember(request):
    for k,v in request.session.items():
            if k in 'username':
                login_user=v
                if request.method == 'POST':
                    group_id=request.POST['group_id']
                    username=request.POST['username']
                    people1=list(Creategroup.objects.all().filter(id=group_id).values_list('created_by', flat=True))
                    if login_user in people1:
                        gp=Grouppeople.objects.get(username=username)
                        gsp=Groupsendmessages(added_left=2, group_id=group_id, sender=username)
                        gsp.save()
                        gp.delete()
                        
                        messages.success(request, 'User removed successfully')
                        return redirect('chathome')
                    else:
                        messages.success(request, "You don't have access")
                        return redirect('chathome')


                    
                



            
                