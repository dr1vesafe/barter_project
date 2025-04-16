from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls', namespace='ads')),
    path('login/', LoginView.as_view(template_name='ads/users/login.html', next_page='ads:index'), name='login'),
    path('logout/', LogoutView.as_view(next_page='ads:index'), name='logout'),
]
