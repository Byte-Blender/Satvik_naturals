from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def register(request):
    """Register new user"""
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Login user"""
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'product_list'))
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('product_list')


@login_required(login_url='login')
def profile(request):
    """User profile page"""
    profile = request.user.profile
    orders = request.user.orders.all().order_by('-created_at')
    
    context = {
        'profile': profile,
        'orders': orders,
    }
    return render(request, 'accounts/profile.html', context)