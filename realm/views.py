from django.views.generic.base import TemplateView
from django.db.models import Q

from houses.models import House


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        houses = House.objects_selling.all()[:10]

        filter_houve_cover = Q(
            content_type__startswith='image/'
        )

        # Add default image to each house
        for house in houses:
            house.cover = house.housefile_set.filter(filter_houve_cover).first()

        context_data['houses'] = houses
        return context_data


class ContactsPageView(TemplateView):
    template_name = "contacts.html"
