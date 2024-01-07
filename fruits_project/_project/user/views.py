from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Supplier, Seller, Container, Item, ContainerItem
from django.utils import timezone
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
#====================================================================================================================
#===========================================CONTAINER===========================================================================
#====================================================================================================================
#====================================================================================================================
def add_container(request):
    container = Container.objects.all()
    context = {'container':container}
    if request.method == "POST":
        supplier_name = request.POST.get('supplier')
        date_str = request.POST.get('date')
        type = request.POST.get('type')
        weight = request.POST.get('weight')

        if not supplier_name:
            messages.warning(request, 'يجب إدخال اسم العميل الخاص بالنقلة')
            return redirect('addcontainer')
        if not weight:
            messages.warning(request, ' ادخل الوزن الخاص بالنقلة')
            return redirect('addcontainer')
        # Check for invalid weight (less than 0)
        if int(weight) < 0:
            messages.warning(request, 'يجب أن يكون وزن النقلة اكبر من الصفر')  # Arabic error message
            return redirect('addcontainer')
        try:
            # Try to get the Supplier instance based on the name
            supplier = Supplier.objects.get(name=supplier_name)
        except Supplier.DoesNotExist:
            # Handle the case where the supplier does not exist
            messages.warning(request, 'العميل غير موجود')
            return redirect('addcontainer')

        if not date_str:
            date = timezone.now().date()
        else:
            try:
                date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.warning(request, 'تاريخ غير صالح. يجب أن يكون الشكل YYYY-MM-DD', extra_tags='warning')
                return redirect('addcontainer')

        # Create a new Container instance with the retrieved Supplier
        Container.objects.create(supplier=supplier, date=date, type=type,con_weight=weight)

        messages.success(request, "تم إضافة نقلة جديدة بنجاح")

    containers = Container.objects.all()

    context = {'containers': containers}
    return render(request, 'add.html', context)
#====================================================================================================================
def container_update(request, id):
    container = None 

    if request.method == "POST":
        supplier = request.POST['supplier']
        date_str = request.POST['date']
        type = request.POST['type']
        try:
            supplier = Supplier.objects.get(name=supplier)
        except Supplier.DoesNotExist:
            # Handle the case where the supplier does not exist
            messages.warning(request, 'العميل غير موجود')
            return redirect('containerupdate',id=id)

        try:
            if date_str:  # Check for date input
                date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            elif not supplier:
                messages.error(request,"اسم العميل غير موجود")
                return redirect('containerupdate', id=id)
            else:
                date = timezone.now().date()  # Set to today's date if not provided

            edit = Container.objects.get(id=id)
            edit.supplier = supplier
            edit.date = date
            edit.type = type
            edit.save()
            messages.success(request, 'تم تعديل بيانات النقلة بنجاح', extra_tags='success')
            return redirect("addcontainer")
        except ValueError:
            messages.warning(request, 'تاريخ غير صالح. يجب أن يكون الشكل YYYY-MM-DD', extra_tags='warning')
            return redirect('containerupdate', id=id)
        except Container.DoesNotExist:
            messages.error(request, 'حدث خطأ، العميل غير موجود', extra_tags='error')
            return redirect("containerupdate")

    else:  # Initial rendering
        try:
            container = Container.objects.get(id=id)  # Retrieve object
        except Container.DoesNotExist:
            messages.error(request, 'حدث خطأ، العميل غير موجود', extra_tags='error')
            return redirect("containerupdate")

    context = {"container": container, "id": id}
    return render(request, 'containerupdate.html', context)

#====================================================================================================================
def container_delete(request,id):
    container_delete = get_object_or_404(Container, id=id )
    if request.method == "POST":
        container_delete.delete()
        return redirect("addcontainer")
    return render(request, 'containerdelete.html')
#====================================================================================================================
def container_details(request, id):
    container = get_object_or_404(Container, pk=id)
    return render(request, 'cardetails.html', {'container': container})
#====================================================================================================================
def container_items(request, id):
    container = get_object_or_404(Container, pk=id)

    if request.method == 'POST':
        form_data = request.POST

        # Validate form data
        try:
            item_name = form_data['item_name']
            count = int(form_data['count'])
            tool = form_data['tool']
            price = float(form_data['price'])

            if not price:
                raise ValueError("الرجاء إدخال السعر")  
            if not count:
                raise ValueError("الرجاء إدخال العدد")  
            if count <= 0 or price <= 0:
                raise ValueError("العدد والسعر يجب أن يكونا أكبر من صفر")

            item = Item.objects.get(name=item_name)
        except ValueError as e:
            messages.error(request, str(e))
        except Item.DoesNotExist:
            messages.error(request, f"الصنف {item_name} غير موجود")
        else:
            # Create a new ContainerItem object
            ContainerItem.objects.create(
                container=container,
                item=item,
                count=count,
                tool=tool,
                price=price
            )
            messages.success(request, "تم إضافة الصنف بنجاح")
            return redirect('containeritems', id)

    return render(request, 'containerItems.html', {'container': container})
#====================================================================================================================
def containeritem_delete(request,id):
    container_item_delete = get_object_or_404(ContainerItem, id=id )
    if request.method == "POST":
        container_item_delete.delete()
        return redirect("containeritems", id=container_item_delete.container.id)
    return render(request, 'containeritemdelete.html',{'container': container_item_delete.container})
#====================================================================================================================
def today_containers(request):
    todays_date = timezone.now().date()  # Get today's date
    containers = Container.objects.filter(date=todays_date)  # Filter by today's date
    context = {'container': containers}  # Pass the filtered queryset to the template

    return render(request, 'today.html', context)
#====================================================================================================================
def remain_containers(request):
    return render(request, 'remain.html')
#====================================================================================================================
def finished_containers(request):
    return render(request, 'finished.html')
#====================================================================================================================
def sell_container(request, id):
    container = get_object_or_404(Container, pk=id)
    return render(request, 'sellcar.html',{'container': container})
#====================================================================================================================
#====================================================================================================================
#=========================== ===================calculations======================================================================
#====================================================================================================================
#====================================================================================================================
def loses(request):
    return render(request, 'loses.html')
#====================================================================================================================
def profits(request):
    return render(request, 'profits.html')
#====================================================================================================================
def day_money(request):
    return render(request, 'daymoney.html')
#====================================================================================================================
#====================================================================================================================
#=============================================ITEMS=======================================================================
#====================================================================================================================
#====================================================================================================================
def add_items(request):
    item = Item.objects.all()
    context = {'item':item}
    if request.method == "POST":
        name = request.POST.get('name')
        date = request.POST.get('date')

        if not name:
            messages.warning(request, 'يجب إدخال اسم الصنف')
            return redirect('items')

        elif not date:
            date = timezone.now().date()
        else:
            try:
                date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                messages.warning(request, 'تاريخ غير صالح. يجب أن يكون الشكل YYYY-MM-DD', extra_tags='warning')
                return redirect('items')

        Item.objects.create(name=name, date=date)

        messages.success(request, "تم إضافة صنف جديد بنجاح")

    # item = Container.objects.all()

    return render(request,"kinds.html",context)
#====================================================================================================================
def item_update(request, id):
    item = None

    if request.method == "POST":
        name = request.POST.get('name')
        date = request.POST.get('date')

        try:
            if date:
                date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            elif not name:
                messages.error(request, "اسم الصنف غير موجود")
                return redirect('itemupdate', id=id)
            else:
                date = timezone.now().date()

            edit = Item.objects.get(id=id)
            edit.name = name
            edit.date = date
            edit.save()
            messages.success(request, 'تم تعديل بيانات الصنف بنجاح', extra_tags='success')
            return redirect("items")
        except ValueError:
            messages.warning(request, 'تاريخ غير صالح. يجب أن يكون الشكل YYYY-MM-DD', extra_tags='warning')
            return redirect('itemupdate', id=id)
        except Item.DoesNotExist:
            messages.error(request, 'حدث خطأ، الصنف غير موجود', extra_tags='error')
            return redirect("itemupdate", id=id)

    else:  # Initial rendering
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            messages.error(request, 'حدث خطأ، الصنف غير موجود', extra_tags='error')
            return redirect("itemupdate", id=id)

    context = {"item": item, "id": id}
    return render(request, 'kindsupdate.html', context)
#====================================================================================================================
def item_delete(request,id):
    item_delete = get_object_or_404(Item, id=id )
    if request.method == "POST":
        item_delete.delete()
        return redirect("items")
    return render(request, 'kindsdelete.html')
#====================================================================================================================
#====================================================================================================================
#===========================================SELLER & SUPPLIER=========================================================================
#====================================================================================================================
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

        if Seller.objects.create(name=name, place=place, date=date):
            messages.success(request, 'تم إضافة بائع جديد بنجاح', extra_tags='success')
        else:
            messages.warning(request, 'حدث خطأ، يرجى التأكد من أن جميع البيانات صحيحة', extra_tags='error')

    return render(request, 'sellersaccounts.html',context)
#====================================================================================================================
def seller_page(request,id):
    seller = get_object_or_404(Seller, id=id)
    context = {'seller': seller}
    return render(request, 'sellerpage.html', context)
#====================================================================================================================
def seller_update(request, id):
    seller = None  # Initialize

    if request.method == "POST":
        name = request.POST['name']
        place = request.POST['place']
        date_str = request.POST['date']

        try:
            if date_str:  # Check for date input
                date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            elif not name:
                messages.error(request,"اسم البائع غير موجود")
                return redirect('sellerupdate', id=id)
            elif not place:
                messages.error(request,"يرجى إدخال المنطقة")
                return redirect('sellerupdate', id=id)
            else:
                date = timezone.now().date()  # Set to today's date if not provided

            edit = Seller.objects.get(id=id)
            edit.name = name
            edit.place = place
            edit.date = date
            edit.save()
            messages.success(request, 'تم تعديل بيانات البائع بنجاح', extra_tags='success')
            return redirect("selleraccounts")
        except ValueError:
            messages.warning(request, 'تاريخ غير صالح. يجب أن يكون الشكل YYYY-MM-DD', extra_tags='warning')
            return redirect('sellerupdate', id=id)
        except Seller.DoesNotExist:
            messages.error(request, 'حدث خطأ، العميل غير موجود', extra_tags='error')
            return redirect("selleraccounts")

    else:  # Initial rendering
        try:
            seller = Seller.objects.get(id=id)  # Retrieve object
        except Seller.DoesNotExist:
            messages.error(request, 'حدث خطأ، العميل غير موجود', extra_tags='error')
            return redirect("selleraccounts")

    context = {"seller": seller, "id": id}
    return render(request, 'sellerupdate.html', context)
#====================================================================================================================
def seller_delete(request,id):
    seller_delete = get_object_or_404(Seller, id=id )
    if request.method == "POST":
        seller_delete.delete()
        return redirect("selleraccounts")
    return render(request, "sellerdelete.html")
#====================================================================================================================
def seller_sort(request):
    seller = Seller.objects.all()
    context = {'seller':seller}
    return render(request, 'sellersort.html', context)
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

        if Supplier.objects.create(name=name, place=place, date=date):
            messages.success(request, 'تم إضافة عميل جديد بنجاح', extra_tags='success')
        else:
            messages.warning(request, 'حدث خطأ، يرجى التأكد من أن جميع البيانات صحيحة', extra_tags='error')

    return render(request, 'suppliersaccounts.html', context)
#====================================================================================================================\
def supplier_sort(request):
    sup = Supplier.objects.all()
    context = {'sup': sup}
    return render(request,'suppliersort.html',context)
#====================================================================================================================
def supplier_page(request, id):
    sup = get_object_or_404(Supplier, id=id)
    containers = sup.container_set.all()
    context = {'sup': sup, 'containers': containers}
    return render(request, 'supplierpage2.html', context)
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
            edit.date = date
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