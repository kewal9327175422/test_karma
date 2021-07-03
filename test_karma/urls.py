"""test_karma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings # need to import to see media file in adime page  
from django.conf.urls.static import static # need to import to see media file in adime page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT) # need to add to see media file in adime page
