from django.contrib import admin
from adminsortable2.admin import SortableAdminBase, SortableStackedInline

from houses import models, forms


admin.site.register(models.Locale)
admin.site.register(models.Parish)
admin.site.register(models.Municipality)
admin.site.register(models.District)
admin.site.register(models.Country)

admin.site.register(models.HouseCondition)
admin.site.register(models.HouseType)
admin.site.register(models.HouseTypology)
admin.site.register(models.EnergyCertificate)


@admin.register(models.HouseFile)
class HouseFileAdmin(admin.ModelAdmin):
    form = forms.HouseFileForm
    ordering = ('-house', 'order')

    list_display = (
        'house',
        'filename',
        'content_type'
    )

    list_filter = (
        'house',
        'content_type',
    )


class HouseFileStackedInline(SortableStackedInline):
    model = models.HouseFile
    form = forms.HouseFileForm


@admin.register(models.House)
class HouseAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [HouseFileStackedInline]

    list_display = (
        'title',
        'type',
        'typology',
        'condition',
        'locale',
        'current_price_in_euros',
        'gross_private_area_in_square_meters',
        'net_internal_area_in_square_meters'
    )

    list_filter = (
        'active',
        'type',
        'typology',
        'condition',
        'locale',
    )
