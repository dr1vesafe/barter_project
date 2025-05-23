from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
import hashlib
import json

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
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        category = self.request.GET.get('category', '')
        condition = self.request.GET.get('condition', '')

        key_data = {
            'query': query, 
            'category': category, 
            'condition': condition
            }
        
        key_str = json.dumps(key_data, sort_keys=True)
        cache_key = 'ads:ad_list'

        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = Ad.objects.all().order_by('-created_at')
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )

            if category:
                queryset = queryset.filter(category=category)

            if condition:
                queryset = queryset.filter(condition=condition)

            cache.set(cache_key, queryset, 60 * 3)

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
class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.cache_clear()
        return response
    
    def cache_clear(self):
        try:
            cache.delete_pattern('ad_list_*')
        except AttributeError:
            pass
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Создание объявления'
        return context


class BaseAdView(LoginRequiredMixin, UserPassesTestMixin):
    model = Ad
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user

# Редактирование объявления
class AdUpdateView(BaseAdView, UpdateView):
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Редактирование объявления'
        return context
    
# Удаления объявления
class AdDeleteView(BaseAdView, DeleteView):
    template_name = 'ads/ad_delete.html'
    
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
    
# Создание предложения
class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/proposal/proposal_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['ad_receiver'] = get_object_or_404(Ad, pk=self.kwargs.get('ad_id'))
        return kwargs
    
    def form_valid(self, form):
        form.instance.ad_receiver = get_object_or_404(Ad, id=self.kwargs['ad_id'])
        form.instance.status = 'pending'
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('ads:proposal_list', kwargs={'pk': self.kwargs['ad_id']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Создание предложения'
        return context
    
# Изменение статуса предложения
class ProposalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExchangeProposal

    def test_func(self):
        proposal = self.get_object()
        return proposal.ad_receiver.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('ads:proposal_list', kwargs={'pk': self.object.ad_receiver.id})
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        new_status = request.GET.get('status')
        if new_status in ['accepted', 'rejected']:
            self.object.status = new_status
            self.object.save()
        return redirect(self.get_success_url())