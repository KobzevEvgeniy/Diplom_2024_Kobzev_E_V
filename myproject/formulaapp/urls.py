from django.urls import path

from .views import new_formula

urlpatterns = [
     path('new_formula/', new_formula, name='new_formula'),
]