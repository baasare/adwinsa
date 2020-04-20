from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),

    # Users
    path('users/', views.user_list, name='users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),

    # Signup
    path('register/', views.register, name='register'),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name="logout"),

    # Password Change
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html',
                                                                   success_url='/password-change-done/'),
         name='password_change'),
    path('password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),

    # Password Forgot Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                                                 from_email='Cedi Kioski <noreply@cedikioski.com>',
                                                                 email_template_name='users/password_reset_email.html',
                                                                 subject_template_name='users/password_reset_subject.txt', ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<slug:uidb64>/<slug:token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
