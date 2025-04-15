from django.contrib import admin

from .models import Ad, ExchangeProposal

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'category', 'condition']
    list_filter = ['category', 'condition', 'created_at']
    search_fields = ['title', 'description']

@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ['ad_sender', 'ad_receiver', 'comment', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['ad_sender', 'ad_receiver']