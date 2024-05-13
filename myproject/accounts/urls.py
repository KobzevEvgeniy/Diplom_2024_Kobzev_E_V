from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgot_password, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.reset_password, name='resetPassword'),

    path('my_formulas/', views.my_formulas, name='my_formulas'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('formula_detail/<formula_id>/', views.formula_detail, name='formula_deteil')
]
