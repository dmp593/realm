from django.db import models
from django.db.models.query import QuerySet


class HouseManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter()


class HouseSellingManager(HouseManager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(active=True, sold_at__isnull=True)
