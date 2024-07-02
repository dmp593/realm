from django.urls import path

from houses import views


urlpatterns = [
    path('', views.HouseListView.as_view(), name='house_list'),
    path('create', views.HouseCreateView.as_view(), name='house_create'),
    path('<int:pk>', views.HouseDetailView.as_view(), name='house_detail'),
    path('upload-chunk', views.ChunkedUploadView.as_view(), name='upload_chunk'),
]
