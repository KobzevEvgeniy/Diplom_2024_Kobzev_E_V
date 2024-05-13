from django.urls import path


from ingredientsapp.views import add_ingredient, edit_ingredient, ingredient_detail, ingredient_list

urlpatterns = [
    path('add_ingredient/', add_ingredient, name='add_ingredient'),
    path('edit_ingredient/', edit_ingredient, name='edit_ingredient'),
    path('ingredient_detail/', ingredient_detail, name='ingredient_detail'),
    path('ingredient_list/', ingredient_list, name='ingredient_list'),


]
