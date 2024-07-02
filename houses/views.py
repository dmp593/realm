import mimetypes
from typing import Any

from django.core.paginator import Paginator
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse_lazy

from houses import models, forms


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
            house.cover = house.housefile_set.filter(filter_houve_cover).first()

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

        for file in obj.housefile_set.all():
            if file.content_type.startswith('image/'):
                obj.images.append(file)

            if file.content_type.startswith('video/'):
                obj.videos.append(file)

        return obj


class HouseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.House
    form_class = forms.HouseForm
    template_name = 'houses/house_create.html'
    success_url = reverse_lazy('house_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_invalid(self, form):
        response = {
            'errors': form.errors,
            'non_field_errors': form.non_field_errors(),
        }

        return JsonResponse(response, status=400)

    def form_valid(self, form):
        self.object = form.save()

        return JsonResponse({
            'house_id': self.object.pk,
            'success_url': self.get_success_url()
        })


class ChunkedUploadView(DetailView):
    queryset = models.House.objects_selling.all()

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        chunk_index = int(request.POST['chunkIndex'])
        total_chunks = int(request.POST['totalChunks'])
        file_id = request.POST['fileId']
        filename = request.POST['filename']
        order = request.POST['order']

        chunk_name = f"{file_id}_chunk_{chunk_index}"
        default_storage.save(chunk_name, ContentFile(file.read()))

        if chunk_index == total_chunks - 1:
            # Combine chunks
            final_file = ContentFile(b'')
            for i in range(total_chunks):
                chunk_name = f"{file_id}_chunk_{i}"
                chunk_file = default_storage.open(chunk_name)
                final_file.write(chunk_file.read())
                chunk_file.close()
                default_storage.delete(chunk_name)

            # Create the HouseFile instance
            house_file = models.HouseFile(
                house_id=self.get_object().pk,
                filename=filename,
                order=order
            )

            # Save the combined file
            final_file_path = models.house_file_upload_to(house_file, filename)
            house_file.file = default_storage.save(final_file_path, final_file)

            # Determine the content type
            content_type, _ = mimetypes.guess_type(final_file_path)
            house_file.content_type = content_type

            house_file.save()

        return JsonResponse({'status': 'ok'})
