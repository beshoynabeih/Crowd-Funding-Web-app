from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='signin.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('setting/change_password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='password_change'),
    path('setting/change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),

    #profile
    path('<int:user_id>/', views.profile, name='profile_page'),
    path('update_user_information/<int:user_id>/', views.update_user_information,name='update_user_information'),
    path('update_project/<int:user_id>/<int:project_id>/', views.update_project,name='update_project'),
    path('delete_project/<int:user_id>/<int:project_id>/',views.delete_project,name='delete_project'),
    path('update_donation/<int:user_id>/<int:donation_id>/',views.update_donation,name='update_donation'),
    path('delete_donation/<int:user_id>/<int:donation_id>/',views.delete_donation,name='delete_donation'),
    path('delete_account/<int:user_id>/',views.delete_account,name='delete_account')
]
