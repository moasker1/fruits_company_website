from django.shortcuts import render, redirect
from .forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    pass    
#====================================================================================================================
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
#====================================================================================================================
def logout_user(request):
    logout(request)
    return render(request, 'logout.html')
#====================================================================================================================
@login_required(login_url="login")
def home(request):
    return render(request, 'home.html')
#====================================================================================================================
def add(request):
    return render(request, 'add.html')
def cardetails(request):
    return render(request, 'cardetails.html')
#====================================================================================================================
def finished(request):
    return render(request, 'finished.html')
#====================================================================================================================
def loses(request):
    pass
#====================================================================================================================
def profits(request):
    pass
#====================================================================================================================
def remain(request):
    return render(request, 'remain.html')
#====================================================================================================================
def sellcar(request):
    return render(request, 'sellcar.html')
#====================================================================================================================
def sellerpage(request):
    return render(request, 'sellerpage.html')
#====================================================================================================================
def selleraccounts(request):
    return render(request, 'sellersaccounts.html')
#====================================================================================================================
def supplierpage(request):
    return render(request, 'supplierpage.html')
#====================================================================================================================
def suppliersaccounts(request):
    return render(request, 'suppliersaccounts.html')
#====================================================================================================================
def today(request):
    return render(request, 'today.html')
#====================================================================================================================