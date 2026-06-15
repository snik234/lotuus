"""
URL configuration for lotus_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from cars.views import home, car_list, car_detail, profile, register, edit_profile, test_drive, add_car, heritage, delete_car


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('cars/', car_list),
    path('cars/<int:id>/', car_detail),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', profile),
    path('register/', register),
    path('profile/edit/', edit_profile),
    path('test-drive/', test_drive, name='test_drive'),
    path('cars/add/', add_car, name='add_car'),
    path('heritage/', heritage, name='heritage'),
    path('cars/delete/<int:car_id>/', delete_car, name='delete_car'),]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)