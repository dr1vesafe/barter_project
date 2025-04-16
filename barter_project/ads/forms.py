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

class ExchangeProposalForm(forms.ModelForm):
    ad_sender = forms.ModelChoiceField(
        queryset=Ad.objects.none(),
        label='Ваше объявление для обмена'
    )
    class Meta:
        model = ExchangeProposal
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Ваш комментарий'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.ad_receiver = kwargs.pop('ad_receiver', None)
        super().__init__(*args, **kwargs)

        if self.request.user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=self.request.user)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request.user:
            ad_sender = Ad.objects.filter(user=self.request.user).first()
            if ad_sender:
                instance.ad_sender = ad_sender
        if self.ad_receiver:
            instance.ad_receiver = self.ad_receiver
        if commit:
            instance.save()
        return instance