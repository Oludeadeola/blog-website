import debug_toolbar
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),
    path('bloggy/', include('blog.urls')),
    path('bloggy/auth/', include('auths.urls')),
]
