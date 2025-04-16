from django.db import models
from django.contrib.auth.models import User

class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('clothes', 'Одежда'),
        ('electronics', 'Электроника'),
        ('jewelry', 'Бижутерия'),
        ('furniture', 'Мебель'),
        ('other', 'Другое'),
    ]

    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image_url = models.URLField(blank=True, null=True, verbose_name='Изображение')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория')
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES, verbose_name='Состояние')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'ad'
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
    ]
    ad_sender = models.ForeignKey(to=Ad, on_delete=models.CASCADE, related_name='sent_proposals', verbose_name='Отправитель предложения')
    ad_receiver = models.ForeignKey(to=Ad, on_delete=models.CASCADE, related_name='received_proposals', verbose_name='Получатель предложения')
    comment = models.TextField(verbose_name='Комментарий')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        db_table = 'proposal'
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'