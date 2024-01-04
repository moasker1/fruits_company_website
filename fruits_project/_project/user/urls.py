from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_user, name='login' ),
    path('logout',views.logout_user, name='logout' ),
    path('register',views.register, name='register' ),
    path('home',views.home, name='home' ),

    path('addcontainer',views.add_container, name='addcontainer' ),
    path('containerdelete/<int:id>',views.container_delete, name='containerdelete' ),
    path('containerupdate/<int:id>',views.container_update, name='containerupdate' ),

    path('cardetails',views.car_details, name='cardetails' ),
    path('finished',views.finished, name='finished' ),
    path('remain',views.remain, name='remain' ),
    path('sellcar',views.sell_car, name='sellcar' ),

    path('sellerpage/<int:id>',views.seller_page, name='sellerpage' ),
    path('selleraccounts',views.seller_accounts, name='selleraccounts' ),
    path('sellerdelete/<int:id>',views.seller_delete, name='sellerdelete' ),
    path('sellerupdate/<int:id>',views.seller_update, name='sellerupdate' ),

    path('supplierpage/<int:id>',views.supplier_page, name='supplierpage' ),
    path('suppliersaccounts',views.suppliers_accounts, name='suppliersaccounts' ),
    path('suppliersdelete/<int:id>',views.supplier_delete, name='suppliersdelete' ),
    path('supplierupdate/<int:id>',views.supplier_update, name='supplierupdate' ),

    path('today',views.today, name='today' ),
]
    