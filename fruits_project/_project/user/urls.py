from django.urls import path
from . import views
# from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',views.login_user, name='login' ),
    path('logout',views.logout_user, name='logout' ),
    path('register',views.register, name='register' ),
    path('home',views.home, name='home' ),
    path('add',views.add, name='add' ),
    path('cardetails',views.cardetails, name='cardetails' ),
    path('finished',views.finished, name='finished' ),
    path('remain',views.remain, name='remain' ),
    path('sellcar',views.sellcar, name='sellcar' ),
    path('sellerpage',views.sellerpage, name='sellerpage' ),
    path('selleraccounts',views.selleraccounts, name='selleraccounts' ),
    path('supplierpage',views.supplierpage, name='supplierpage' ),
    path('suppliersaccounts',views.suppliersaccounts, name='suppliersaccounts' ),
    path('today',views.today, name='today' ),
]
