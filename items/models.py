from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=255, verbose_name='Описание')
    price = models.IntegerField(default=0, verbose_name='Цена')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100) # В центах

    def get_absolute_url(self):
        return reverse('landing-page', kwargs={'item_slug': self.slug})
