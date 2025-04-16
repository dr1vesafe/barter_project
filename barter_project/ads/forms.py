from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название товара'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описание'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://example.com/image.jpg'}),
            'category': forms.Select(choices=Ad.CATEGORY_CHOICES),
            'condition': forms.Select(choices=Ad.CONDITION_CHOICES),
        }