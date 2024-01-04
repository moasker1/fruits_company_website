from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Supplier
from django.utils import timezone

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
    sup = Supplier.objects.all()
    context = {'sup': sup}
    return render(request, 'supplierpage.html', context)
#====================================================================================================================
@login_required(login_url="login")
# views.py
def suppliersaccounts(request):
    sup = Supplier.objects.all()
    context = {'sup': sup}

    if request.method == "POST":
        name = request.POST.get('name')
        place = request.POST.get('place', 'غير محدد')  
        date_str = request.POST.get('date')

        if not name:
            messages.warning(request, 'يجب إدخال اسم العميل')
            return redirect('suppliersaccounts')

        if Supplier.objects.filter(name=name).exists():
            messages.warning(request, 'اسم العميل موجود بالفعل في قاعدة البيانات')
            return redirect('suppliersaccounts')

        if not date_str:
            date = timezone.now().date()
        else:
            try:
                date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.warning(request, 'تاريخ غير صالح. يجب أن يكون الشكل YYYY-MM-DD', extra_tags='warning')
                return redirect('suppliersaccounts')

        if Supplier.objects.create(name=name, place=place, date_created=date):
            messages.success(request, 'تم إضافة عميل جديد بنجاح', extra_tags='success')
        else:
            messages.warning(request, 'حدث خطأ، يرجى التأكد من أن جميع البيانات صحيحة', extra_tags='error')

    return render(request, 'suppliersaccounts.html', context)
#====================================================================================================================
def suppliersDelete(request,id):
    supplier_delete = get_object_or_404(Supplier, id=id )
    if request.method == "POST":
        supplier_delete.delete()
        return redirect("suppliersaccounts")
    return render(request, 'suppliersdelete.html')

#====================================================================================================================
def today(request):
    return render(request, 'today.html')
#====================================================================================================================