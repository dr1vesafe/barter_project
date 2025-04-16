from django.urls import path
from .views import *

app_name = 'ads'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ads', AdListView.as_view(), name='ad_list'),
    path('registration', RegistrationView.as_view(), name='registration'),
    path('ads/creation/', AdCreationView.as_view(), name='ad_creation'),
    path('ads/update/<int:pk>/', AdUpdateView.as_view(), name='ad_update'),
    path('ads/delete/<int:pk>/', AdDeleteView.as_view(), name='ad_delete'),
]
