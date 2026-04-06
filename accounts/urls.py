from django.urls import path
from .views import RegisterView, LoginView, RequestOTPView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]