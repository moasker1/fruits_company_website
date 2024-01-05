from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_user, name='login' ),
    path('logout',views.logout_user, name='logout' ),
    path('register',views.register, name='register' ),
    path('home',views.home, name='home' ),
# =====================================================================================
    path('addcontainer',views.add_container, name='addcontainer' ),
    path('containerdelete/<int:id>',views.container_delete, name='containerdelete' ),
    path('containerupdate/<int:id>',views.container_update, name='containerupdate' ),
    path('condetails',views.container_details, name='cardetails' ),
    path('containerItems/<int:id>',views.container_items, name='containeritems' ),
    path('today',views.today_containers, name='today' ),
    path('remain',views.remain_containers, name='remain' ),
    path('finished',views.finished_containers, name='finished' ),
    path('sellcon',views.sell_container, name='sellcar' ),
# =====================================================================================
    path('profits',views.profits, name='profits' ),
    path('loses',views.loses, name='loses' ),
    path('daymoney',views.day_money, name='daymoney' ),
# =====================================================================================
    path('items',views.add_items, name='items' ),
    path('itemupdate/<int:id>',views.item_update, name='itemupdate' ),
    path('itemdelete/<int:id>',views.item_delete, name='itemdelete' ),
# =====================================================================================
    path('sellerpage/<int:id>',views.seller_page, name='sellerpage' ),
    path('selleraccounts',views.seller_accounts, name='selleraccounts' ),
    path('sellerdelete/<int:id>',views.seller_delete, name='sellerdelete' ),
    path('sellerupdate/<int:id>',views.seller_update, name='sellerupdate' ),
# =====================================================================================
    path('supplierpage/<int:id>',views.supplier_page, name='supplierpage' ),
    path('suppliersaccounts',views.suppliers_accounts, name='suppliersaccounts' ),
    path('suppliersort',views.supplier_sort, name='suppliersort' ),
    path('suppliersdelete/<int:id>',views.supplier_delete, name='suppliersdelete' ),
    path('supplierupdate/<int:id>',views.supplier_update, name='supplierupdate' ),
]
    