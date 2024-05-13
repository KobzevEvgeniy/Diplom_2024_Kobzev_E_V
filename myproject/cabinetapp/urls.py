from django.urls import path

from .views import cabinet_index

urlpatterns = [
     path('cabinet_index/', cabinet_index, name='cabinet_index'),
]