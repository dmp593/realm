"""
URL configuration for realm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from realm.views import HomePageView, ContactsPageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),

    path('i18n/', include('django.conf.urls.i18n')),
    
    path('admin/', admin.site.urls),
    path('houses/', include('houses.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
