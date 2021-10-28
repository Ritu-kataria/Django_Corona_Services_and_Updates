from django.urls import path
from users import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('hospital_dashboard', views.hospital_dashboard, name='hospital_dashboard'),
    path('update_profile', views.ProfileUpdateView.as_view(), name='update_profile'),
]