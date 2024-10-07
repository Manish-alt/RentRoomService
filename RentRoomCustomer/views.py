from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_bookmark = current_user.old_bookmark
            if saved_bookmark:
                converted_bookmark = json.loads(saved_bookmark)
                bookmark = Cart(request)
                for key, value in converted_bookmark.items():
                    bookmark.db_add(product=key)
            
            messages.success(request, ('You have been logged in'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error, please try again'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have Registered Successfully. Welcome"))
            return redirect('update_info')
        else:
            messages.success(request, ('Oops there was a problem registering. Please try again.'))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form': form})
    
    
def product(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(id=pk)
        return render(request, 'product.html', {'product':product})
    else:
        messages.success(request, "User is not logged in.")
        return redirect('login')

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name = foo)
        products = Product.objects.filter(category = category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ("Category Doesn't exist"))
        return redirect('home')
    
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, "User has been updated")
            return redirect('home')
        return render(request, 'update_profile.html', {'user_form': user_form})
    else:
        messages.success(request, 'Something went wrong')
        return redirect('home')
            
        
        
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request)
            if form.is_valid():
                form.save()
                messages.success(request, "Password changed Successfully")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
                
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})

    else:
        return redirect('home')
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, "User Info has been updated")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, 'Something went wrong')
        return redirect('home')
    

def search(request):
    if request.method =="POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched))
        
        if not searched:
            messages.success(request, "Searched room doesn't exists.")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})
