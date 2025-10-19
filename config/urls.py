from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('films/', include('films.urls')), 

    path('', RedirectView.as_view(url='/films/', permanent=False)),
]