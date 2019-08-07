from django.db import models

# Create your models here.


class Import(models.Model):
    """Выгрузка"""
    value = models.TextField()