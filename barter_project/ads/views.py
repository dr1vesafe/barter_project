from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Ad, ExchangeProposal
from .forms import AdForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView, ListView, FormView, CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Главная страница
class IndexView(TemplateView):
    template_name = 'ads/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Главная'
        return context

# Страница со списком объявлений
class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'page_obj'
    paginate_by = 5

    def get_queryset(self):
        queryset = Ad.objects.all().order_by('-created_at')
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )

        if category:
            queryset = queryset.filter(category__icontains=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Список объявлений'
        return context
    

# Регистрация пользователя
class RegistrationView(FormView):
    template_name = 'ads/users/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('ads:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Регистрация'
        return context
    
class AdCreationView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
