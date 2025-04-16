from django.urls import path
from .views import *

app_name = 'ads'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ad_list', AdListView.as_view(), name='ad_list'),
    path('registration', RegistrationView.as_view(), name='registration'),
    path('ad_creation', AdCreationView.as_view(), name='ad_creation'),
]
