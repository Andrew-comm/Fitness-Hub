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
    
    path('enrollment/', views.enrollment_form, name='enrollment'),
    path('virtual-classes/', views.virtual_classes, name='virtual_classes'),
    path('suggest_workout/', views.suggest_workout, name='workout_form'),
    path('generate-workout/', views.generate_workout, name='generate_workout'),

    path('community/', views.community_feed_list, name='community_feed'),
    path('create-post', views.community_feed_create, name='create-post'),
    path('comments/<int:post_id>/', views.add_comment, name='comments'), 
    path('likes/<int:post_id>/', views.like_post, name='like_post'), 
    path('record/', views.record_session, name='record_session'),

    
    path('log-progress/', views.log_progress, name='log-progress'),
    path('dashboard/', views.dashboard, name='dashboard'),



]