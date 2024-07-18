from django.urls import path

from houses import views


app_name = 'houses'


urlpatterns = [
    path('', views.HouseListView.as_view(), name='list'),
    path('<int:pk>', views.HouseDetailView.as_view(), name='detail'),
]
