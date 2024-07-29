from django.db import models
from django.utils.translation import gettext_lazy as _

from .locations import Country


class CountryTax(models.Model):
    country = models.ForeignKey(
        to=Country,
        on_delete=models.PROTECT,
        verbose_name=_('country'),
    )

    tax_rate = models.DecimalField(
        verbose_name=_('tax rate'),
        max_digits=4,
        decimal_places=2
    )

    class Meta:
        verbose_name = _('country tax')
        verbose_name_plural = _('country taxes')
        ordering = ['country', 'tax_rate']

    def __str__(self):
        return f"{self.country.name}: {self.tax_rate}%"


class PricingTier(models.Model):
    country_tax = models.ForeignKey(
        to=CountryTax,
        on_delete=models.PROTECT,
        verbose_name=_('country tax'),
    )

    lower_bound = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,  # Allow null for the lower bound to represent open-ended ranges
        blank=True,
        verbose_name=_('lower bound')
    )

    upper_bound = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,  # Allow null for the upper bound to represent open-ended ranges
        blank=True,
        verbose_name=_('upper bound')
    )

    gross_cost_in_euros = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=False,
        verbose_name=_('gross cost in euros')
    )

    def _net_cost_in_euros(self):
        tax_rate = 1 + (self.country_tax.tax_rate / 100)
        return round(self.gross_cost_in_euros * tax_rate, 2)

    _net_cost_in_euros.short_description = _('net cost in euros')

    net_cost_in_euros = property(_net_cost_in_euros)

    class Meta:
        verbose_name = _('pricing tier')
        verbose_name_plural = _('pricing tiers')
        ordering = ['gross_cost_in_euros']

    def __str__(self):
        _from = _('from')
        _to = _('to')

        if self.lower_bound and self.upper_bound:
            return f"{_from} {self.lower_bound} {_to} {self.upper_bound}: {self.gross_cost_in_euros}€"
        
        if self.lower_bound:
            return f"{_from} {self.lower_bound}: {self.gross_cost_in_euros}€"
        
        if self.upper_bound:
            return f"{_to} {self.upper_bound}: {self.gross_cost_in_euros}€"
        
        return f"{self.gross_cost_in_euros}€"
