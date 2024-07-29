import pathlib
import mimetypes

from uuid import uuid4

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from houses.models.locations import Locale
from houses.managers import HouseManager, HouseSellingManager


REGEX_PORTUGUESE_POSTAL_CODE = r'\d{4}-\d{3}'


def house_file_upload_to(instance: 'HouseFile', filename: str) -> str:
    instance.filename = filename

    extension = mimetypes.guess_extension(filename)

    if not extension:
        extension = pathlib.Path(filename).suffix

    content_type, _ = mimetypes.guess_type(filename)

    if content_type:
        instance.content_type = content_type

    return f"houses/{instance.house.pk}/{uuid4().hex}{extension}"


class HouseType(models.Model):
    parent = models.ForeignKey(
        to='self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
        related_query_name='child',
        verbose_name=_('parent type')
    )

    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('name'),
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('house type')
        verbose_name_plural = _('houses types')
        ordering = ['parent__name', 'name']


class HouseTypology(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('name'),
    )

    order = models.IntegerField(
        null=False,
        verbose_name=_('order'),
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('house typology')
        verbose_name_plural = _('houses typologies')
        ordering = ['order', 'name',]


class HouseCondition(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('name'),
    )

    order = models.IntegerField(
        null=False,
        verbose_name=_('order'),
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('house condition')
        verbose_name_plural = _('house conditions')
        ordering = ['order', 'name',]


class EnergyCertificate(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('name'),
    )

    order = models.IntegerField(
        null=False,
        verbose_name=_('order'),
    )

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = _('energy certificate')
        verbose_name_plural = _('energy certificates')
        ordering = ['order', 'name',]


class House(models.Model):
    title = models.CharField(
        max_length=150,
        null=False,
        verbose_name=_('title'),
    )

    description = models.TextField(
        null=False,
        verbose_name=_('description'),
    )

    address = models.CharField(
        max_length=255,
        null=False,
        verbose_name=_('address'),
    )

    postal_code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                REGEX_PORTUGUESE_POSTAL_CODE,
                message=_('Not a valid postal-code. Pattern must be: XXXX-XXX')
            )
        ],
        null=False,
        verbose_name=_('postal code'),
    )

    locale = models.ForeignKey(
        to=Locale,
        on_delete=models.PROTECT,
        null=False,
        verbose_name=_('locale'),
    )

    type = models.ForeignKey(
        to=HouseType,
        on_delete=models.PROTECT,
        null=False,
        verbose_name=_('type'),
    )

    price_in_euros = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=False,
        verbose_name=_('price in euros'),
    )

    discount_in_euros = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('discount in euros'),
    )

    typology = models.ForeignKey(
        to=HouseTypology,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('typology'),
    )

    condition = models.ForeignKey(
        to=HouseCondition,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('condition'),
    )

    gross_private_area_in_square_meters = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ],
        null=True,
        blank=True,
        verbose_name=_('gross private area in square meters'),
    )

    net_internal_area_in_square_meters = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ],
        null=True,
        blank=True,
        verbose_name=_('net internal area in square meters'),
    )

    construction_year = models.IntegerField(
        validators=[
            MinValueValidator(1800)
        ],
        null=True,
        blank=True,
        verbose_name=_('construction year'),
    )

    number_of_rooms = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ],
        null=True,
        blank=True,
        verbose_name=_('number of rooms'),
    )

    number_of_bathrooms = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ],
        null=True,
        blank=True,
        verbose_name=_('number of bathrooms'),
    )

    has_garage = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('has garage'),
    )

    garage_included_in_price = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('garage included in price')
    )

    has_pool = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('has pool')
    )

    has_terrace = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('has terrace')
    )

    has_balcony = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('has balcony')
    )

    has_garden = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('has garden')
    )

    floor_level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('floor level')
    )

    has_lift = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('has lift')
    )

    adapted_for_reduced_mobility = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_('is adapted for people with reduced mobility')
    )

    energy_certificate = models.ForeignKey(
        to=EnergyCertificate,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_('energy certificate'),
    )

    highlighted = models.BooleanField(
        default=False,
        verbose_name=_('highlighted'),
    )

    reserved = models.BooleanField(
        default=False,
        verbose_name=_('reserved')
    )

    active = models.BooleanField(
        default=True,
        verbose_name=_('active'),
    )

    sold_at = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('sold at'),
    )

    sold_for = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('sold for'),
    )

    order = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('order'),
    )

    @property
    def current_price_in_euros(self):
        if not self.discount_in_euros:
            return self.price_in_euros
        
        return self.price_in_euros - self.discount_in_euros

    def __str__(self):
        return f"{self.title}"

    objects = HouseManager()
    objects_selling = HouseSellingManager()

    class Meta:
        verbose_name = _('house')
        verbose_name_plural = _('houses')
        ordering = ['-highlighted', 'order', '-pk', ]


class HouseFile(models.Model):
    house = models.ForeignKey(
        to=House,
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_('house'),
        related_name='files',
        related_query_name='file'
    )

    file = models.FileField(
        upload_to=house_file_upload_to,
        null=False,
        verbose_name=_('file'),
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('description'),
    )

    filename = models.CharField(
        max_length=255,
        editable=False,
        verbose_name=_('filename'),
    )

    content_type = models.CharField(
        max_length=50,
        editable=False,
        verbose_name=_('content type'),
    )

    order = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('order'),
    )

    def __str__(self):
        return f"{self.filename}"

    class Meta:
        verbose_name = _('house file')
        verbose_name_plural = _('house files')
        ordering = ['order',]
