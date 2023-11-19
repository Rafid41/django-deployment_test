from django import forms
from django.contrib.auth.models import User
from Login_app.models import UserInfo

class UserForm(forms.ModelForm):
    # password box e "..." dekhabe actual password na dekhaya
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model = User
        #built in model and form
        fields = ('username','email','password')


class UserInfoForm(forms.ModelForm):
    class Meta():
        model = UserInfo
        fields = ('facebook_id','profile_pic')