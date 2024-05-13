from django.core.checks import messages
from django.core.paginator import Paginator
from django.db.models import Max, Min
from django.shortcuts import render, get_object_or_404

from .forms import IngredientForm
from .models import Ingredient


def add_ingredient(request):
    if request.method == 'POST':
        ingredient = IngredientForm(request.POST)
        if ingredient.is_valid():
            name = request.POST['name']
            index_e = request.POST['index_e']
            description = request.POST['description']
            price = request.POST['price']
            quantity = request.POST['quantity']
            image = request.POST['image']
            brix = request.POST['brix']
            manufacturer = request.POST['manufacturer']
            supplier = request.POST['supplier']
            unit_of_measure = request.POST['unit_of_measure']
            added_date = request.POST['added_date']
            ingredient = Ingredient.objects.create_ingredient(name=name, index_e=index_e, description=description,
                                                              price=price, quantity=quantity, image=image, brix=brix,
                                                              manufacturer=manufacturer, supplier=supplier,
                                                              unit_of_measure=unit_of_measure,
                                                              added_date=added_date)
        ingredient.save()
        messages.success(request, 'Ингредиент успешно сохранен!')
    else:
        ingredient = IngredientForm()

    context = {
        'ingredient': ingredient,
    }
    return render(request, 'ingredientsapp/add_ingredient.html', context)


def edit_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.order_by('ingredient_id')

    if request.method == 'POST':
        ingredient_form = IngredientForm(request.POST, ingredient_id=ingredient_id)

        if ingredient_form.is_valid():
            ingredient.name = request.POST['name']
            ingredient.index_e = request.POST['index_e']
            ingredient.description = request.POST['description']
            ingredient.price = request.POST['price']
            ingredient.quantity = request.POST['quantity']
            ingredient.image = request.POST['image']
            ingredient.brix = request.POST['brix']
            ingredient.manufacturer = request.POST['manufacturer']
            ingredient.supplier = request.POST['supplier']
            ingredient.unit_of_measure = request.POST['unit_of_measure']
            ingredient.added_date = request.POST['added_date']

            ingredient_form.save()
            ingredient.save()

            messages.success(request, 'Ингредиент успешно обновлен')
            return render(request, 'ingredientsapp/edit_ingredient.html')


def ingredient_detail(request, ingredient_id):
    ingredient = Ingredient.objects.filter_by(ingredient_id=ingredient_id)
    if request.method == 'GET':
        context = {
            'ingredient.name': ingredient.name,
            'ingredient.image': ingredient.image,
            'ingredient.description': ingredient.description,
            'ingredient.quantity': ingredient.quantity,
            'ingredient.unit_of_measure': ingredient.unit_of_measure,
            'ingredient.brix': ingredient.brix,
            'ingredient.supplier': ingredient.supplier,
            'ingredient.manufacturer': ingredient.manufacturer
        }
        return render(request, 'ingredient/ingredient_detail.html', context)


def paginator(request, ingredient_list, ingredient_per_page):
    """
    Paginate pages
    :param request:
    :param ingredient_list: List of all ingredients
    :param ingredient_per_page: How many ingredients per page show
    :return: Number of ingredients displayed
    """
    ingredient_paginator = Paginator(ingredient_list, ingredient_per_page)
    page = request.GET.get('page')
    paged_ingredients = ingredient_paginator.get_page(page)
    return paged_ingredients


def ingredient_list(request, description_slug=None, ingredient=None):
    """
    Render 'ingredient list' page where show all ingredients by description.
    :param request:
    :param description_slug: description
    :return: Render ingredient_list.html
    """
    description = None
    ingredients = None

    # Sidebar panel (ingredients amount, price range)
    all_ingredients_count = Ingredient.objects.all().count()
    max_price_placeholder = Ingredient.objects.aggregate(Max('price'))['price__max']
    min_price_placeholder = Ingredient.objects.aggregate(Min('price'))['price__min']

    if description_slug is not None:
        description = get_object_or_404(Ingredient, slug=ingredient.description)
        if 'min_price' in request.GET:
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            if min_price == '':
                min_price = 0
            if max_price == '':
                max_price = Ingredient.objects.aggregate(Max('price'))['price__max']
            ingredients = Ingredient.objects.filter(price__range=(min_price, max_price), description=description,
                                                    is_available=True).order_by('id')
            paged_ingredients = paginator(request, ingredients, 6)
            ingredients_count = ingredients.count()
        else:
            ingredients = Ingredient.objects.filter(description=description, is_available=True).order_by('id')
            paged_ingredients = paginator(request, ingredients, 6)
            ingredients_count = ingredients.count()
    else:
        if 'min_price' in request.GET:
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            if min_price == '':
                min_price = 0
            if max_price == '':
                max_price = Ingredient.objects.aggregate(Max('price'))['price__max']
            ingredients = Ingredient.objects.all().filter(is_available=True,
                                                          price__range=(min_price, max_price)).order_by('id')
            paged_ingredients = paginator(request, ingredients, 6)
            ingredients_count = ingredients.count()
        else:
            ingredients = Ingredient.objects.all().filter(is_available=True).order_by('id')
            paged_ingredients = paginator(request, ingredients, 6)
            ingredients_count = ingredients.count()

    context = {
        'ingredients': paged_ingredients,
        'ingredients_count': ingredients_count,
        'all_ingredients_count': all_ingredients_count,
        'max_price_placeholder': max_price_placeholder,
        'min_price_placeholder': min_price_placeholder
    }
    return render(request, 'ingredientsapp/ingredient_list.html', context)
