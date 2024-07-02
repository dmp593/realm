from django.urls import path

from houses import views


urlpatterns = [
    path('', views.HouseListView.as_view(), name='house_list'),
    path('<int:pk>', views.HouseDetailView.as_view(), name='house_detail'),

    path('create', views.HouseCreateView.as_view(), name='house_create'),
    path('<int:pk>/upload', views.ChunkedUploadView.as_view(), name='house_file_upload'),
]
