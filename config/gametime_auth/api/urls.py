from django.urls import path

from gametime_auth.api.views import UserDetail

urlpatterns = [
    path("users/<str:email>", UserDetail.as_view(), name="user-detail"),
]
