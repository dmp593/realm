from typing import Any

from django.core.paginator import Paginator
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView

from houses import models


class HouseListView(ListView):
    queryset = models.House.objects_selling.all()
    context_object_name = "houses"
    paginate_by = 10  # Number of houses per page

    def get_queryset(self):
        queryset = super().get_queryset()

        search_term = self.request.GET.get('search')

        if search_term:
            reference = search_term
            
            if search_term.startswith('#'):
                reference = search_term[1:]

            if reference.isnumeric():
                qs = queryset.filter(pk=int(reference))

                if qs.exists():
                    return qs

        district_id = self.request.GET.get('district')
        municipality_id = self.request.GET.get('municipality')
        parish_id = self.request.GET.get('parish')
        locale_id = self.request.GET.get('locale')
        typology_id = self.request.GET.get('typology')
        type_id = self.request.GET.get('type')

        if district_id:
            queryset = queryset.filter(locale__parish__municipality__district_id=district_id)
        
        if municipality_id:
            queryset = queryset.filter(locale__parish__municipality_id=municipality_id)
        
        if parish_id:
            queryset = queryset.filter(locale__parish_id=parish_id)

        if locale_id:
            queryset = queryset.filter(locale_id=locale_id)
        
        if typology_id:
            queryset = queryset.filter(typology_id=typology_id)
        
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(address__icontains=search_term) |
                Q(postal_code__icontains=search_term)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        houses = paginator.get_page(page_number)

        filter_houve_cover = Q(
            content_type__startswith='image/'
        )

        # Add default image to each house
        for house in houses:
            house.cover = house.files.filter(filter_houve_cover).first()

        context['houses'] = houses

        # Fetch districts, municipalities, parishes, typologies, and types
        context['districts'] = models.District.objects.all()
        context['municipalities'] = models.Municipality.objects.all()
        context['parishes'] = models.Parish.objects.all()
        context['locales'] = models.Locale.objects.all()
        context['types'] = models.HouseType.objects.all()
        context['typologies'] = models.HouseTypology.objects.all()

        return context


class HouseDetailView(DetailView):
    queryset = models.House.objects_selling.all()
    context_object_name = "house"

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Model:
        obj = super().get_object(queryset)

        obj.images = []
        obj.videos = []

        for file in obj.files.all():
            if file.content_type.startswith('image/'):
                obj.images.append(file)

            if file.content_type.startswith('video/'):
                obj.videos.append(file)

        return obj


class HouseFacebookPost(CreateView):
    ...