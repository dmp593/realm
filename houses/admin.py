import requests

from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy as _n

from realm.utils import get_facebook_page_id, get_facebook_page_access_token
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

    def upload_house_images_to_facebook(self, house: models.House) -> list[str]:
        page_id = get_facebook_page_id()
        access_token = get_facebook_page_access_token()

        upload_url = f'https://graph.facebook.com/v13.0/{page_id}/photos'
        images = house.files.filter(content_type__startswith='image/').all()[:3]

        photos_ids = []

        for image in images:
            params = {
                'access_token': access_token,
                'published': 'false',
                'url': image.file.url,
            }

            response = requests.post(upload_url, params=params)
            response.raise_for_status()

            result = response.json()
            photos_ids.append(result['id'])

        return photos_ids

    def post_house_on_facebook(self, house):
        # Step 1: Upload photos with published state set to false
        photos_ids = self.upload_house_images_to_facebook(house)

        # Step 2: Create a post with the uploaded unpublished images IDs
        page_id = get_facebook_page_id()
        access_token = get_facebook_page_access_token()

        post_url = f"https://graph.facebook.com/{page_id}/feed"
        post_payload = {
            'message': house.description,
            'access_token': access_token
        }

        for i, photo_id in enumerate(photos_ids):
            post_payload[f'attached_media[{i}]'] = f'{{"media_fbid":"{photo_id}"}}'

        response = requests.post(post_url, json=post_payload)
        response.raise_for_status()

    @admin.action(description=_('Post on Facebook'))
    def post_on_facebook(self, request, queryset):
        try:
            for house in queryset.all():
                self.post_house_on_facebook(house)

            n = queryset.count()

            self.message_user(
                request,
                _n(
                    "%d house was successfully published on facebook.",
                    "%d houses were successfully published on facebook.",
                    n,
                )
                % n,
                messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request,
                _('Something failed while publishing to facebook. Please check your feed.'),
                messages.ERROR,
            )
