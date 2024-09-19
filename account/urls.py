from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    # Account Urls

    path('verify-phone/', views.verify_phone, name='verify-phone'),
    path('verify-code/', views.verify_code, name='verify-code'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.profile, name='profile'),
    path('edite-account-information', views.edite_account_information, name='edite_account_information'),
    path('verify-new-phone', views.verify_new_phone, name='verify-new-phone'),
    path('verify-new-code', views.verify_new_phone_code, name='verify-new-phone_code'),

]