from django.urls import path
from auths.views import BloggerCreateUpdateView, SuperUserCreateUpdateView
from django.urls import include

urlpatterns = [
    path('register-blogger/', BloggerCreateUpdateView.as_view()),
    path('create-superuser/', SuperUserCreateUpdateView.as_view()),
    path('token/', include('auths.token.urls'))
]
