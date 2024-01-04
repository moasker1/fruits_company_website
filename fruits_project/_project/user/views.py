from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Supplier, Seller
from django.utils import timezone
from django.http import JsonResponse
# from datetime import datetime 

#====================================================================================================================
#====================================================================================================================
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
#====================================================================================================================
def car_details(request):
    return render(request, 'cardetails.html')
#====================================================================================================================
def finished(request):
    return render(request, 'finished.html')
#====================================================================================================================
def today(request):
    return render(request, 'today.html')
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
def sell_car(request):
    return render(request, 'sellcar.html')
#====================================================================================================================
def seller_accounts(request):
    seller = Seller.objects.all()
    context = {'seller': seller}

    if request.method == "POST":
        name = request.POST.get('name')
        place = request.POST.get('place', 'غير محدد')  
        date_str = request.POST.get('date')

        if not name:
            messages.warning(request, 'يجب إدخال اسم البائع')
            return redirect('selleraccounts')
        if not place:
            messages.warning(request, 'برجاء إدخال اسم المنطقة')
            return redirect('selleraccounts')

        if Seller.objects.filter(name=name).exists():
            messages.warning(request, 'اسم البائع موجود بالفعل في قاعدة البيانات')
            return redirect('selleraccounts')

        if not date_str:
            date = timezone.now().date()
        else:
            try:
                date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.warning(request, 'تاريخ غير صالح. يجب أن يكون الشكل YYYY-MM-DD', extra_tags='warning')
                return redirect('selleraccounts')

        if Seller.objects.create(name=name, place=place, date_created=date):
            messages.success(request, 'تم إضافة بائع جديد بنجاح', extra_tags='success')
        else:
            messages.warning(request, 'حدث خطأ، يرجى التأكد من أن جميع البيانات صحيحة', extra_tags='error')

    return render(request, 'sellersaccounts.html',context)
#====================================================================================================================
def seller_page(request):
    return render(request, 'sellerpage.html')
#====================================================================================================================
@login_required(login_url="login")
def suppliers_accounts(request):
    sup = Supplier.objects.all()
    context = {'sup': sup}

    if request.method == "POST":
        name = request.POST.get('name')
        place = request.POST.get('place', 'غير محدد')  
        date_str = request.POST.get('date')

        if not name:
            messages.warning(request, 'يجب إدخال اسم العميل')
            return redirect('suppliersaccounts')
        if not place:
            messages.warning(request, 'برجاء إدخال اسم المنطقة')
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
def supplier_page(request,id):
    sup = Supplier.objects.get(id=id)
    context = {'sup': sup}
    return render(request, 'supplierpage.html', context)
#====================================================================================================================
def supplier_update(request, id):
    sup = None  # Initialize sup

    if request.method == "POST":
        name = request.POST['name']
        place = request.POST['place']
        date_str = request.POST['date']

        try:
            if date_str:  # Check for date input
                date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            elif not name:
                messages.error(request,"اسم العميل غير موجود")
                return redirect('supplierupdate', id=id)
            elif not place:
                messages.error(request,"يرجى إدخال المنطقة")
                return redirect('supplierupdate', id=id)
            else:
                date = timezone.now().date()  # Set to today's date if not provided

            edit = Supplier.objects.get(id=id)
            edit.name = name
            edit.place = place
            edit.date_created = date
            edit.save()
            messages.success(request, 'تم تعديل بيانات العميل بنجاح', extra_tags='success')
            return redirect("suppliersaccounts")
        except ValueError:
            messages.warning(request, 'تاريخ غير صالح. يجب أن يكون الشكل YYYY-MM-DD', extra_tags='warning')
            return redirect('supplierupdate', id=id)
        except Supplier.DoesNotExist:
            messages.error(request, 'حدث خطأ، العميل غير موجود', extra_tags='error')
            return redirect("suppliersaccounts")

    else:  # Initial rendering
        try:
            sup = Supplier.objects.get(id=id)  # Retrieve object
        except Supplier.DoesNotExist:
            messages.error(request, 'حدث خطأ، العميل غير موجود', extra_tags='error')
            return redirect("suppliersaccounts")

    context = {"sup": sup, "id": id}
    return render(request, 'supplierupdate.html', context)
#====================================================================================================================
def supplier_delete(request,id):
    supplier_delete = get_object_or_404(Supplier, id=id )
    if request.method == "POST":
        supplier_delete.delete()
        return redirect("suppliersaccounts")
    return render(request, 'suppliersdelete.html')
#====================================================================================================================