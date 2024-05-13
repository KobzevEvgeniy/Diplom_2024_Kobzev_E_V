from datetime import datetime
from typing import Dict, Any

from django.contrib.postgres.fields import ArrayField
from django.shortcuts import redirect, render

from .models import FormulaIngredients, Formula

formula_number = None


def new_formula(request, ingredient=None, total_dry_matter_product=None, total_price_product=None):
    current_user = request.user
    formula_items = FormulaIngredients.objects.filter(user=current_user)
    formula_count = formula_items.count()
    if formula_count <= 0:
        return redirect('new_formula')
    if request.method == 'POST':
        formula = Formula(request.POST)
        formula_ingredient = ArrayField(FormulaIngredients(request.POST))

        if formula.is_valid():
            data = Formula()
            data.user = current_user
            data.first_name = formula.cleaned_data['first_name']
            data.last_name = formula.cleaned_data['last_name']
            data.phone = formula.cleaned_data['phone']
            data.email = formula.cleaned_data['email']
            data.date_added = datetime.now().strftime('%Y%m%d')
            data.recipe_status = formula.cleaned_data['recipe_status']
            data.status_success = formula.cleaned_data['status_success']
            data.description_formula = formula.cleaned_data['description_formula']
            data.name_product = formula.cleaned_data['name_product']
            data.description_product = formula.cleaned_data['description_product']
            data.save()
            formula_ingredient.formula = data
            formula_ingredient.ingredient = formula_ingredient.choese(ingredient)
            formula_ingredient.brix = formula_ingredient.brix
            formula_ingredient.quantity_1 = formula_ingredient.cleaned_data['quantity_1']
            formula_ingredient.unit_of_measure = formula_ingredient.unit_of_measure
            formula_ingredient.dry_matter = formula_ingredient.brix * formula_ingredient.quantity_1
            formula_ingredient.price = formula_ingredient.price
            formula_ingredient.index_e = formula_ingredient.index_e
            formula_ingredient.save()
            total_price_product = 0
            for ingredient in formula_ingredient:
                total_price_product += ingredient.price * formula_ingredient.quantity_1
            return total_price_product

            total_dry_matter_product = 0
            for formula_ingredient in formula_ingredients:
                total_dry_matter_product += formula_ingredient.dry_matter
            return total_dry_matter_product

        context = {
                'full_name': formula.user,
                'recipe_status': formula.recipe_status,
                'date_added': formula.date_added,
                'name_product': formula.name_product,
                'status_success': formula.status_success,
                'stage': ingredient.stage,
                'ingredient': ingredient.name,
                'BRIX': ingredient.brix,
                'total_dry_matter_product': total_dry_matter_product,
                'quantity_1': ingredient.quantity_1,
                'unit_of_measure': ingredient.unit_of_measure,
                'price': ingredient.price,
                'level_in_total_volume': ingredient.level_in_total_volume,
                'total_price_product': total_price_product,
                'description_formula': formula.description_formula,
                'description_product': formula.description_product

            }
        return render(request, 'new_formula', context)
