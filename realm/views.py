from pathlib import Path

from django.views.generic.base import TemplateView, View
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
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


class ChunkedUploadView(View):
    combine_chunks: bool = True

    def get_file_chunk_name(self, file_id: str, file_name: str, chunk_index: int, total_chunks: int) -> str:
        return f"{file_id}_chunk_{chunk_index}"

    def get_combined_file_name(self, file_id: str, file_name: str, total_chunks: int):
        return f"uploads/{file_id}/{file_name}"

    def save_file_chunk(self, file_chunk_name: str, file_chunk: UploadedFile):
        default_storage.save(file_chunk_name, ContentFile(file_chunk.read()))

    def combine_files_chunks(self, combined_file_name: str, total_chunks: int, file_id: str, file_name: str):
        # Combined chunks
        file = ContentFile(b'')

        for chunk_index in range(total_chunks):
            file_chunk_name = self.get_file_chunk_name(file_id, file_name, chunk_index, total_chunks)

            with default_storage.open(file_chunk_name) as file_chunk:
                file.write(file_chunk.read())

            default_storage.delete(file_chunk_name)

        # Save the combined file
        default_storage.save(combined_file_name, file)

    def file_upload_finished(self, request, filename: str, *args, **kwargs):
        ...

    def post(self, request, *args, **kwargs):
        file_chunk = request.FILES.get('file')
        file_id = request.POST.get('fileId')
        file_name = request.POST.get('fileName', request.POST.get('filename'))

        chunk_index = int(request.POST['chunkIndex'])
        total_chunks = int(request.POST['totalChunks'])

        file_chunk_name = self.get_file_chunk_name(file_id, file_name, chunk_index, total_chunks)
        self.save_file_chunk(file_chunk_name, file_chunk)

        if chunk_index == total_chunks - 1:
            combined_file_name = self.get_combined_file_name(file_id, file_name, total_chunks)

            if self.combine_chunks:
                self.combine_files_chunks(combined_file_name, total_chunks, file_id, file_name)

            self.file_upload_finished(request, combined_file_name, *args, **kwargs)

            return JsonResponse({
                'status': 'ok',
                'url': default_storage.url(file_chunk_name)
            })

        return JsonResponse({'status': 'ok'})


class FileUploadView(ChunkedUploadView):
    combine_chunks: bool = False

    def get_file_chunk_name(self, file_id: str, file_name: str, chunk_index: int, total_chunks: int) -> str:
        return f"uploads/{file_id}/{file_name}"

    def save_file_chunk(self, file_chunk_name: str, file_chunk: UploadedFile):
        if not default_storage.exists(file_chunk_name):
            default_storage.save(file_chunk_name, ContentFile(file_chunk.read()))
            return

        with default_storage.open(file_chunk_name, 'ab') as f:
            f.write(file_chunk.read())
