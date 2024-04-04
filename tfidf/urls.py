from django.urls import include, path

urlpatterns = [
    path('', include('loader.urls')),
]
