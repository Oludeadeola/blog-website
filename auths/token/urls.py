from django.urls import path

from auths.token import views

urlpatterns = [
    path("create/", views.TokenCreateView.as_view()),
    path("refresh/", views.TokenRefreshView.as_view()),
]
