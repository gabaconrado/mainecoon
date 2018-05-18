'''
xScratch URL patterns
'''
from django.urls import path

from . import views

app_name = 'xs'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('sign_in/', views.SignInView.as_view(), name='sign_in'),
    path('sign_out/', views.SignOutView.as_view(), name='sign_out'),
    path('learn/', views.LearnView.as_view(), name='learn'),
    path('script/', views.ScriptView.as_view(), name='script'),
]
