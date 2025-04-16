from django.urls import path
from .views import *

app_name = 'ads'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ads', AdListView.as_view(), name='ad_list'),
    path('user/registration', RegistrationView.as_view(), name='registration'),
    path('user/profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('ads/create/', AdCreateView.as_view(), name='ad_create'),
    path('ads/update/<int:pk>/', AdUpdateView.as_view(), name='ad_update'),
    path('ads/delete/<int:pk>/', AdDeleteView.as_view(), name='ad_delete'),
    path('ads/<int:pk>', AdPageView.as_view(), name='ad_page'),
    path('proposals/list/<int:pk>/', ProposalListView.as_view(), name='proposal_list'),
    path('proposals/create/<int:ad_id>/', ProposalCreateView.as_view(), name='proposal_create'),
]
