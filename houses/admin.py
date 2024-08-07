from django.http import HttpRequest
import requests

from django.urls import reverse
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy as _n

from facebook.utils import get_facebook_page_id, refresh_facebook_tokens
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


admin.site.register(models.CountryTax)


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


class HouseFileStackedInline(admin.StackedInline):
    model = models.HouseFile
    form = forms.HouseFileInlineForm


@admin.register(models.House)
class HouseAdmin(admin.ModelAdmin):
    form = forms.HouseForm
    inlines = [HouseFileStackedInline]
    actions = (
        'post_on_facebook',
    )
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

    def upload_house_images_to_facebook(self, page_id: str, access_token: str, request: HttpRequest, house: models.House, max_images_to_upload: int = 3) -> list[str]:
        upload_url = f'https://graph.facebook.com/v20.0/{page_id}/photos'

        realm_host = request.get_host()
        house_images = house.files.filter(content_type__startswith='image/').all()
        
        photos_ids = []
        nr_images_uploaded = 0

        for house_image in house_images:
            if nr_images_uploaded >= max_images_to_upload:
                break

            if house_image.file.size > 419_430_4:
                # max facebook image size to upload is 4MB
                continue

            response = requests.post(
                upload_url,
                json={
                    'access_token': access_token,
                    'url': f"https://{realm_host}{house_image.file.url}",
                    'published': 'false',
                }
            )

            response.raise_for_status()

            result = response.json()
            photo_id = result['id']

            photos_ids.append(photo_id)
            nr_images_uploaded += 1

        return photos_ids

    def post_house_on_facebook(self, page_id, access_token, request, house):
        # Step 1: Upload photos with published state set to false
        photos_ids = self.upload_house_images_to_facebook(page_id, access_token, request, house, max_images_to_upload=1)

        # Step 2: Create a post with the uploaded unpublished images IDs
        host = request.get_host()
        house_detail_url = reverse('houses:detail', args=[house.pk])
        url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
        payload = {
            'access_token': access_token,
            'message': f"*** {house.title} ***\n\n{house.description}",
            'link': f"https://{host}{house_detail_url}",
            'attached_media': [{'media_fbid': photo_id} for photo_id in photos_ids],
            'published': True
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()

    @admin.action(description=_('Post on Facebook'))
    def post_on_facebook(self, request, queryset):
        try:
            facebook_page_id = get_facebook_page_id()
            fb_user_access_token, fb_page_access_token = refresh_facebook_tokens()

            for house in queryset.all():
                self.post_house_on_facebook(facebook_page_id, fb_page_access_token, request, house)
            
            n = queryset.count()
            
            self.message_user(
                request,
                _n(
                    "%d house was successfully published on Facebook.",
                    "%d houses were successfully published on Facebook.",
                    n,
                ) % n,
                messages.SUCCESS,
            )

        except Exception as e:
            self.message_user(
                request,
                _('Something failed while publishing to Facebook. Please check your feed.'),
                messages.ERROR,
            )


@admin.register(models.PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    form = forms.PricingTierForm

    list_display = (
        'country_tax',
        'lower_bound',
        'upper_bound',
        'gross_cost_in_euros',
        'net_cost_in_euros',
    )

    list_filter = (
        'country_tax',
    )
