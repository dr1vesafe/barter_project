from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Ad, ExchangeProposal
from .forms import AdForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
    paginate_by = 3

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

# Создание объявления
class AdCreationView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Создание объявления'
        return context
    
# Редактирование объявления
class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Редактирование объявления'
        return context
    
# Удаления объявления
class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_delete.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Удаление объявления'
        return context
    
# Личный кабинет пользователя
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'ads/users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['head_title'] = 'Личный кабинет'
        context['ads'] = Ad.objects.filter(user=user)
        context['sent_proposals'] = ExchangeProposal.objects.filter(ad_sender__user=user)
        context['received_proposals'] = ExchangeProposal.objects.filter(ad_receiver__user=user)

        return context
    
# Страница объявления
class AdPageView(DetailView):
    model = Ad
    template_name = 'ads/ad_page.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = self.object.title
        return context
    
# Список предложений
class ProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'ads/proposal/proposal_list.html'
    context_object_name = 'proposals'

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) |
            Q(ad_receiver__user=self.request.user)
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Список предложений'
        return context