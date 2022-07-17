from django.urls import path

from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('my-account/', views.user_account, name='my-account'),
    path('edit-account/', views.edit_account, name='edit-account'),

    path('add-skill/', views.create_skill, name='add-skill'),
    path('update-skill/<str:pk>/', views.update_skill, name='update-skill'),

]