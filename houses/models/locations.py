from django.db import models
from django.utils.translation import gettext_lazy as _


REGEX_PORTUGUESE_POSTAL_CODE = r'\d{4}-\d{3}'


class Country(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('name')
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        ordering = ['name']


class District(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('name')
    )

    country = models.ForeignKey(
        to=Country,
        on_delete=models.PROTECT,
        verbose_name=_('country')
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.country}"

    class Meta:
        verbose_name = _('district')
        verbose_name_plural = _('districts')
        ordering = ['country__name', 'name']
        unique_together = [
            ['country', 'name',]
        ]


class Municipality(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('name')
    )

    district = models.ForeignKey(
        to=District,
        on_delete=models.PROTECT,
        verbose_name=_('district')
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.district}"

    class Meta:
        verbose_name = _('municipality')
        verbose_name_plural = _('municipalities')
        ordering = ['district__country__name', 'district__name', 'name',]
        unique_together = [
            ['district', 'name',]
        ]


class Parish(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('name')
    )

    municipality = models.ForeignKey(
        to=Municipality,
        on_delete=models.PROTECT,
        verbose_name=_('municipality')
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.municipality}"

    class Meta:
        verbose_name = _('parish')
        verbose_name_plural = _('parishes')
        ordering = [
            'municipality__district__country__name',
            'municipality__district__name',
            'municipality__name',
            'name',
        ]
        unique_together = [
            ['municipality', 'name',]
        ]


class Locale(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_('name')
    )

    parish = models.ForeignKey(
        to=Parish,
        on_delete=models.PROTECT,
        verbose_name=_('parish')
    )
    
    def __str__(self) -> str:
        return f"{self.name}, {self.parish}"

    class Meta:
        verbose_name = _('locale')
        verbose_name_plural = _('locales')
        ordering = [
            'parish__municipality__district__country__name',
            'parish__municipality__district__name',
            'parish__municipality__name',
            'parish__name',
            'name'
        ]
        unique_together = [
            ['parish', 'name',]
        ]
