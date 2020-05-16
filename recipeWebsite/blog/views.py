from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Recipe, Ingredient
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib import messages

from django.http import Http404, HttpResponse, HttpResponseRedirect

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_recipe_list'

    def get_queryset(self):
        return Recipe.objects.order_by('-pub_date')[:10]

class DetailView(generic.DetailView):
    template_name = 'blog/detail.html'
    model = Recipe

def Register(request, error_message=None):
    return render(request, 'blog/register.html')

def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    try: 
        User.objects.create_user(username, email, password)
        user = authenticate(request, username=username, password=password)
        login(request,user)
        return HttpResponseRedirect(reverse('blog:index'))
    except IntegrityError:
        messages.error(request, "Username is already taken :(")#Try the xml chek username in realtime
        return HttpResponseRedirect(reverse('blog:register'))

def Auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        #Redirect to a home page
        return HttpResponseRedirect(reverse('blog:index'))
    else:
        #Send an error message
        messages.error(request, "Username or Password incorrect/invalid")
        return HttpResponseRedirect(reverse('blog:login'))

def Login(request):
    return render(request, 'blog/login.html')
        
def log_out(request):
    logout(request)
    #Redirect to a login page
    return HttpResponseRedirect(reverse('blog:login'))

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password updated successfully")
        else:
            messages.error(request, "Please correct the error below")
    return HttpResponseRedirect(reverse('blog:profile'))

class ProfileView(generic.ListView):
    template_name = 'blog/profile.html'
    