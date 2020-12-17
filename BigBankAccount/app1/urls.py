from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('process_money/',views.process_money),
    path('reset/',views.reset),
    path('no_more_coins',views.no_more_coins),
    path('add_coins',views.add_coins),
    path('display_login',views.display_login),  
    path('display_register',views.display_register),
    path('display_invest',views.display_invest),
    path('display_account',views.display_account),
    path('increase_investment',views.increase_investment),
    path('invest',views.invest),
    path('withdraw',views.withdraw),
    path('login',views.login),
    path('register',views.register),
    path('logout',views.logout),
    
]
