from django.shortcuts import render
from .models import Ad, ExchangeProposal
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView, ListView

class IndexView(TemplateView):
    template_name = 'ads/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Главная'
        return context

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