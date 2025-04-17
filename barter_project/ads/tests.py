import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad, ExchangeProposal
from django.core.cache import cache

@pytest.mark.django_db
def test_ad_list_view(client):
    url = reverse('ads:ad_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Объявления' in response.content.decode()

@pytest.mark.django_db
def test_create_ad(client):
    user = User.objects.create_user(username='user1', password='1234')
    client.login(username='user1', password='1234')

    response = client.post(reverse('ads:ad_create'), {
        'title': 'Тестовое объявление',
        'description': 'Тестовое описание',
        'category': 'electronics',
        'condition': 'new',
    })

    assert response.status_code == 302
    assert Ad.objects.filter(title='Тестовое объявление').exists()

@pytest.mark.django_db
def test_create_proposal(client):
    sender = User.objects.create_user(username='sender', password='1234')
    receiver = User.objects.create_user(username='receiver', password='1234')

    sender_ad = Ad.objects.create(title='Объявление отправителя', user=sender, category='jewelry', condition='used')
    receiver_ad = Ad.objects.create(title='Оъявление получателя', user=receiver, category='furniture', condition='new')

    client.login(username='sender', password='1234')

    response = client.post(reverse('ads:proposal_create', args=[receiver_ad.id]), {
        'ad_sender': sender_ad.id,
        'comment': 'Не хочешь обменяться?',
    })

    assert response.status_code == 302
    assert ExchangeProposal.objects.filter(ad_sender=sender_ad, ad_receiver=receiver_ad).exists()

@pytest.mark.django_db
def test_cache(client):
    user = User.objects.create_user(username='user1', password='1234')
    cache_key = 'ads:ad_list'
    cache.clear()

    Ad.objects.create(
        user=user,
        title='Тестовое объявление', 
        description='Тестирование кеша', 
        category='other', 
        condition='new')

    response = client.get(reverse('ads:ad_list'))
    assert response.status_code == 200

    cached_response = cache.get(cache_key)
    assert cached_response is not None