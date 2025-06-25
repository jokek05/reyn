from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from chat import views as chat_view

urlpatterns = [
    path('', views.index, name='index'),  # список чатов
    path('chat/<int:chat_id>/', views.chat_view, name='chat'),
    path('chat/<int:chat_id>/delete/', views.delete_chat, name='delete_chat'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('contacts/', views.contact_list, name='contacts'),
    path('contacts/add/', views.add_contact, name='add_contact'),
    path('contacts/add/<int:user_id>/', views.add_contact, name='add_contact'),
    path('add_contact/<int:user_id>/', views.add_contact, name='add_contact'),
    
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/', views.profile_view, name='profile_self'),  
    path('profile/id/<int:user_id>/', views.profile_view_by_id, name='profile_by_id'),
    path('chat_with_user/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('contact/edit/<int:contact_id>/', views.edit_contact_name, name='edit_contact_name'),

    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('message/<int:msg_id>/delete/', views.delete_message, name='delete_message'),
]
