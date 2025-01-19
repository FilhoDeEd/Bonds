from django.urls import path
from account.views import (
    RegisterView,
    LoginView,
    DetailAccountView,
    UpdateAccountBaseView,
    AnonymizeAccountView,
    UpdateNeighborhoodView,
    UpdateAccountEmailView,
    UpdateAccountPasswordView,
    UpdateAccountProfileImage
)


urlpatterns = [
    path('detail/', DetailAccountView.as_view(), name='account_detail'),
    path('register/', RegisterView.as_view(), name='account_register'),
    path('login/', LoginView.as_view(), name='account_login'),
    path('update/', UpdateAccountBaseView.as_view(), name='account_update'),
    path('update-neighborhood/', UpdateNeighborhoodView.as_view(), name='update_neighborhood'),
    path('update-email/', UpdateAccountEmailView.as_view(), name='update_email'),
    path('update-password/', UpdateAccountPasswordView.as_view(), name='update_password'),
    path('update-profile-image/', UpdateAccountProfileImage.as_view(), name='update_profile_image'),
    path('anonymize/', AnonymizeAccountView.as_view(), name='account_anonymize')
]
