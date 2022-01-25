from home.models import Post, Profile
from django import forms




class Editprofile(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('description',)





class Editpost(forms.ModelForm):
    class Meta:
        model=Post
        fields=('description',)


class Editvideopost(forms.ModelForm):
    class Meta:
        model=Post
        fields=('video_description',)




class Updateprofilephoto(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('profilephoto',)