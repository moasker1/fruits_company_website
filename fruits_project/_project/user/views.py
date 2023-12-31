from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register(request):
    form = UserCreationForm()
    return render(request, 'login.html',{'form':form})
    
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'هناك خطأ في اسم المستخدم او كلمة المرور')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return render(request, 'logout.html')

def home(request):
    return render(request, 'home.html')
