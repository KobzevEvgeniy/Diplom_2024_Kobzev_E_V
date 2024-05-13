import datetime

from django import forms

from ingredientsapp.models import Ingredient


class IngredientForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    quantity = forms.IntegerField()
    image = forms.ImageField()
    index_e = forms.CharField(max_length=12)
    brix = forms.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = forms.CharField(max_length=40)
    supplier = forms.CharField(max_length=40)

    unit_of_measure = forms.ChoiceField(choices=[
        ("л", "литр"),
        ("кг", "килограмм"),
        ("т", "тонна"),
        ("шт", "штук"),
    ])
    added_date = forms.DateField(initial=datetime.date.today)

    def save(self):
        cleaned_data = self.cleaned_data
        ingredient = Ingredient.objects.create(
            name=cleaned_data['name'],
            description=cleaned_data['description'],
            price=cleaned_data['price'],
            quantity=cleaned_data['quantity'],
            image=cleaned_data['image'],
            index_e=cleaned_data['index_e'],
            brix=cleaned_data['brix'],
            manufacturer=cleaned_data['manufacturer'],
            supplier=cleaned_data['supplier'],
            unit_of_measure=cleaned_data['unit_of_measure'],
            added_date=cleaned_data['added_date'],

        )
        ingredient.save()
        return ingredient
