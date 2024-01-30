from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.view_profile, name='profile'),  # Updated URL pattern for view_profile
    path('create-profile/', views.create_profile, name='create_profile'),  # Updated URL pattern for create_profile
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile/delete/<int:pk>/', views.delete_profile, name='delete_profile'),   
    path('', views.home, name='home'),
    path('gallery/', views.Gallery_view, name='gallery'),
    path('enrollment/', views.enrollment_form, name='enrollment'),
    path('virtual-classes/', views.virtual_classes, name='virtual_classes'),
    path('suggest_workout/', views.suggest_workout, name='workout_form'),
    path('generate-workout/', views.generate_workout, name='generate_workout'),



]