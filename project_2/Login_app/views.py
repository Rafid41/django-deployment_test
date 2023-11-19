from django.shortcuts import render
from Login_app.forms import UserForm, UserInfoForm
from Login_app.models import UserInfo
from django.contrib.auth.models import User

# for html login page

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def index(request):

    dict = {}
    # views.py er fn er vitor jodi check kora lage j login kora kina
    if request.user.is_authenticated:
        current_user = request.user # fetch logged_in users info in current_user

        print(current_user.username) 
        print(current_user.email)
        print(current_user.id) # primary key of that user in database
        # prints in console after refresh the page in browser:
        # rafid
        # wap.alnahiyan425@gmail.com
        # 1

        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        # NOTE: in UserInfo.objects.get(user__pk=user_id)
        # Structure: "relationship_Variable"+ "__" + "j table er sathe relationship kora hoise tar column"
        # here in model.py, in UserInfo fn, "user" is used to make one-to-one relationship
        # in relashipships, evabe use kora hy
        # "user" holo "UserInfo" er column
        # "pk" holo "User" er column
        # "__" diye separate kora hoy column 2ta
        # "user_id" match korbe "pk" er sathe
       

        dict = {
            "user_basic_info": user_basic_info,
            "user_more_info": user_more_info,
        }

    return render(request, 'Login_app/index.html', dict)


def register(request):

    registered = False

    # form submit korle
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        user_info_form = UserInfoForm(data = request.POST)

        if user_form.is_valid() and user_info_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)  # encrypt password 
            user.save()  # update password with encrypted password


            user_info = user_info_form.save(commit=False) # false rakhle direct db te jabe na, hold kore rakhbe. it's used to collect the informaton in user_info variable
            user_info.user = user  
            #user table and user_info table er entry relate korbe
            # mane user_info class er "user filed" "user" object er sathe connct kore
            # "user" object e ase "user_form" er information
            # "user_info" object e ase "user_info_form" er information


            #check files
            # profile picture upload korse kina
            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic'] # request.FILES['profile_pic'] eta diye file k 'profile_pic' folder e upload kore
            
            user_info.save()
            registered = True

    
    # initially submit korar age
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    dict = {'user_form': user_form, 'user_info_form': user_info_form, 'registered':registered }
    return render(request, 'Login_app/register.html', context= dict)




def login_page(request):
    return render(request, 'Login_app/login.html', context= {})


# er form direct html diye ashbe
def user_login(request):
    if request.method == 'POST':

        # ekhane get('username') er 'username' holo login.html er <input name="username"/>
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate username and password with database
        user = authenticate(username=username, password=password)

        if user:
            # id active kina
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Login_app:index'))
            
                # NOTE 1.: ekhane HttpResponseRedirect use kora hoise cz, etay "view"(page content) + "url pattern"(browser er url box) change kore
                # return render(request, 'Login_app/index.html', context= {}) or return index(request) ei 2ta "just view" change kore, urlpattern ager tai thake 
                # means, se jabe index.html file ei, bt url e dekhabe login.html

                # NOTE 2. reverse() function urls.py er urlpatterns=[] er "name" dhore call korar shubidha dey
                # mane index.html dhore call na kore 'Login_app:index' dhore call korte pari
            else:
                return HttpResponse("Account is not active!")
            
        else:
            return HttpResponse("Invalid username or password!")

    # jodi form submit na hoy
    else:
        return HttpResponseRedirect(reverse('Login_app:login'))
    


# log out korar jnno user logged in thakte hbe must
# decorators to check if user logged_in or not
# used to control views for loggedin or logged_out users
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:index'))