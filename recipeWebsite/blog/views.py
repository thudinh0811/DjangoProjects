from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Recipe, Ingredient, Instruction
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied

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
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully")
        else:
            messages.error(request, "Please correct the error below")
    return HttpResponseRedirect(reverse('blog:profile'))

class ProfileView(LoginRequiredMixin, generic.ListView):
    redirect_field_name =""
    template_name = 'blog/profile.html'
    model = Recipe
    context_object_name='my_recipe_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PasswordChangeForm(self.request.user)
        return context

    def get_queryset(self):
        return Recipe.objects.filter(author__username=self.request.user.username)

class EditView(LoginRequiredMixin, generic.DetailView):
    redirect_field_name =""
    template_name='blog/edit.html'
    model = Recipe
    
    def get_queryset(self):
        query = super(EditView, self).get_queryset()
        return query.filter(author=self.request.user)


    def post(self, request, pk):
        if request.POST['op'] == "delete":
            recipe = get_object_or_404(Recipe, pk=pk)
            recipe.delete()
            return HttpResponseRedirect(reverse('blog:profile'))
        read_recipe_form(request, request.POST, id=pk)
        messages.info(request, "Recipe updated!")
        return HttpResponseRedirect(reverse('blog:edit', args=(pk,)))
    

class AddView(LoginRequiredMixin, generic.View):
    redirect_field_name=""
    template_name = 'blog/add.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        read_recipe_form(request, request.POST, id=None)
        messages.info(request, "Recipe saved!")
        return HttpResponseRedirect(reverse('blog:profile'))


def read_recipe_form(request, form, id=None):
    if id is not None:
        recipe = get_object_or_404(Recipe, pk=id)
        recipe.ingredient_set.all().delete() #Delete then replace with new one
        recipe.instruction_set.all().delete()
    else:
        recipe = Recipe(author = request.user, pub_date=timezone.now())

    current = None

    for item in form: #request.POST --> dictionary

        if item == "recipe_name":
            recipe.recipe_name = form[item]
            recipe.save()

        elif item.startswith("ingredient_name"):
            ingredient = Ingredient(ingredient_name = form[item], ingredient_amount="",recipe=recipe)
            current = ingredient

        elif item.startswith("ingredient_amount"):
            ingredient=current
            ingredient.ingredient_amount = form[item]
            ingredient.save()

        elif item.startswith("instruction"):
            instruction = Instruction(instruction_step=form[item], recipe = recipe)
            instruction.save()
    return 

        



