from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import Post, Profile, Comment
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from home.forms import Editprofile,Editpost, Editvideopost
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from home.serializers import Userserializer
from rest_framework.generics import ListAPIView

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import os


# Create your views here.
@login_required(login_url='login')
def home(request):
    
    
    
    for k,v in request.session.items():
        if k in 'username':
            usern=User.objects.get(username=v)
            pp=Profile.objects.all()
            p=Profile.objects.get(username=v)
            c=Comment.objects.all().order_by('-uploaded_on')[:6]
            usern=usern
           
              
            po=Post.objects.all().order_by('-uploaded_on')

            
            dict={'usern':usern,'post':po,'pp':pp,'co':c,'p':p}
            


            return render(request,'home.html',dict)

@login_required(login_url='login')

def post(request):
    post=Post.objects.filter(username='praveen')
    dict={'post':post}


    return render(request, 'home.html',dict)






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
            return HttpResponse("invalid credentials or account doesn't exists")
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
        d=request.POST['description']
        if User.objects.filter(username=u):
            return HttpResponse("username already exists")
        elif Profile.objects.filter(username=u):
            return HttpResponse("record already exists")
        elif User.objects.filter(email=u):
            return HttpResponse("email already exists")

        elif p1==p2:
            pho=Profile.objects.create(username=u, profilephoto=ph,description=d)
            user=User.objects.create_user(email=e,first_name=f,username=u, password=p1)
            
            user.save()
            pho.save()

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
            po=Post.objects.filter(username=usern).order_by('-uploaded_on')
            c=Comment.objects.all().order_by('-uploaded_on')[:5]


            
            dict={'usern':usern,'post':po,'pp':pp,'co':c,'count':count}
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
                return HttpResponse('Post uploaded successfully')
    
    return render(request,'upload/uploadphoto.html')


@login_required(login_url='login')
def uploadstatus(request):
    
    if request.method=='POST':
        for k,v in request.session.items():
            if k in 'username':
                u=v
               
                s=request.POST['status']

                            
                po=Post(username=u,status=s)
                po.save()
                return HttpResponse('Post uploaded successfully')
    
    return render(request,'upload/uploadstatus.html')







@login_required(login_url='login')

def userspecificprofile(request,name):
    for k,v in request.session.items():
        if k in 'username':
            
            opp=Profile.objects.get(username=v)
    
  
            usern=User.objects.get(username=name)
            pp=Profile.objects.get(username=name)

                    
            username=usern
                
                    
            po=Post.objects.filter(username=usern).order_by('-uploaded_on')
            count=Post.objects.filter(username=usern).count()

                    
            dict={'usern':usern,'post':po,'pp':pp,'opp':opp, 'count':count}
            return render(request,'userspecificprofile.html',dict)


@login_required(login_url='login')

def editprofile(request):
    for k,v in request.session.items():
        if k in 'username':
            
    
            u=v 
            pp=Profile.objects.get(username=v)
            form=Editprofile(instance=pp)
            dict={'form':form,'username':u}
            if request.method == 'POST':
                u=request.POST['username']
                d=request.POST['description']
                if User.objects.filter(username=u):
                   return HttpResponse('username alreadu exists, try any other username')
                
                else:


                    userinputpost=Post.objects.filter(username=v).update(username=u)
                    userinputprofile=Profile.objects.filter(username=v).update(username=u,description=d)
                    userinputcomment=Comment.objects.filter(username=v).update(username=u)

                    
                    user=User.objects.filter(username=v).update(username=u)

                  

                    return HttpResponse('saved successfully. Login again to see the changes')
        
            return render(request, 'edit/editprofile.html',dict)



@login_required(login_url='login')

def deletepost(request,id):
    p=Post.objects.get(id=id)
    co=Comment.objects.filter(postid=id)
    p.delete()
    co.delete()
    return HttpResponse('deleted successfully')






@login_required(login_url='login')
def editpost(request, id):
    s=Post.objects.get(id=id)
    form=Editpost(instance=s)
    dict={'form':form}
    if request.method=="POST":
        userinput=Editpost(request.POST, instance=s)
        if userinput.is_valid():
            userinput.save()
            return HttpResponse('saved successfully')

    return render(request,'edit/editpost.html',dict)



@login_required(login_url='login')

def addcomment(request,id):
    if request.method == 'POST':
        for k,v in request.session.items():
            if k in 'username':
                p=request.POST['postid']
                c=request.POST['comment']
                username=v
                userinput=Comment.objects.create(username=v,postid=p,comment=c)
                userinput.save()
                return redirect('home')


@login_required(login_url='login')
def deleteaccount(request, name):
    u=User.objects.get(username=name)
    p=Profile.objects.get(username=name)
    po=Post.objects.filter(username=name)
    co=Post.objects.filter(username=name)
    u.delete()
    p.delete()
    po.delete()
    co.delete()
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
                ph= Profile.objects.get(username=v)
                if request.method=='POST':
                    if len(ph.profilephoto) >0:
                        os.remove(ph.profilephoto.path)
                        p=request.FILES['profilephoto']
                        ph.profilephoto=p
                        d='Changed profilepicture'
                        ph.save()
                        po=Post(username=v, photos=p, description=d) 
                        po.save()
                        return HttpResponse('saved successfully')
                    
                        
                        
                        
                       
                    
    
   
    

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
                return HttpResponse('Post uploaded successfully')
    
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

