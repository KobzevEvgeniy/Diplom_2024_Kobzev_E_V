from django import forms

from .models import Formula


class FormulaForm(forms.ModelForm):
    class Meta:
        model = Formula
        fields = ['first_name', 'last_name', 'recipe_status', 'status_success', 'stage',
                  'description_formula', 'name_product', 'description_product', 'ingredient']
