from django.contrib import admin

from django.db.models import FileField
from image_uploader_widget.widgets import ImageUploaderWidget
from image_uploader_widget.admin import OrderedImageUploaderInline

from houses import models


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
    formfield_overrides = {
        FileField: {'widget': ImageUploaderWidget},
    }


class HouseFileInlineAdmin(OrderedImageUploaderInline):
    model = models.HouseFile


@admin.register(models.House)
class HouseAdmin(admin.ModelAdmin):
    inlines = [HouseFileInlineAdmin]

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
