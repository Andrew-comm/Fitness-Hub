from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<int:pk>/', views.view_profile, name='profile'),
    path('update-profile/<int:pk>/', views.update_profile, name='update-profile'),       
    path('', views.home, name='home'),
    path('gallery/', views.Gallery_view, name='gallery'),
    path('enrollment/', views.enrollment_form, name='enrollment'),
    path('virtual-classes/', views.virtual_classes, name='virtual_classes'),



]