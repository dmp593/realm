from django import forms
from houses.models import House


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = [
            'title',
            'description',

            'address',
            'postal_code',

            'price_in_euros',
            'discount_in_euros',

            'locale',
            'type',
            'typology',
            'condition',
            'energy_certificate',

            'gross_private_area_in_square_meters',
            'net_internal_area_in_square_meters',

            'construction_year',

            'number_of_rooms',
            'number_of_bathrooms',
            'has_garage',

            'active',
            'highlighted',
            'reserved',
        ]
