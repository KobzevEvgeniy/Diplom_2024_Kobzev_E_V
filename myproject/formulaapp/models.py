from django.contrib import admin
from django.db import models

from ingredientsapp.models import Ingredient
from accounts.models import Account

class Formula(models.Model):
    """class of Formula"""
    objects = models.Manager()

    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    RECIPE_STATUS_CHOICES = [
        ("Н", "новая"),
        ("Д", "доработка"),
        ("У", "утвержденная"),

    ]
    recipe_status = models.CharField(max_length=1, choices=RECIPE_STATUS_CHOICES)

    STATUS_SUCCESS = [
        ('S', 'success'),
        ('F', 'fail'),
    ]
    status_success = models.CharField(max_length=1, choices=STATUS_SUCCESS)
    description_formula = models.TextField(verbose_name='Технологический процесс')
    name_product = models.TextField(max_length=100, verbose_name='Название полученного продукта')
    description_product = models.TextField(verbose_name='Описание полученного продукта')
    product_photo = models.ImageField(upload_to='myproject/media/product', default='default_image.png', blank=True,
                                      verbose_name='Изображение готового продукта')


    @admin.display(description='Фамилия Имя разработчика')
    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    def info_date_added(self):
        return f'{self.date_added}'

    # def __str__(self):
    #     return (f'Дата опыта: {self.date_added},\n'
    #             f'Фамилия Имя разработчика: {self.full_name},\n'
    #             f'Статус успеха: {self.status_success},\n'
    #             f'Технологический процесс: {self.description_formula},\n'
    #             f'Название полученного продукта: {self.name_product},\n'
    #             f'Описание полученного продукта: {self.description_product},\n'
    #             f'Стадия разработки: {self.recipe_status}')

    class Meta:
        verbose_name = 'Рецептура'
        verbose_name_plural = 'Рецептуры'


class FormulaIngredients(models.Model):
    """class of FormulaIngredients"""
    objects = models.Manager()
    STAGE_CHOICES = [
        ("A", "первый"),
        ("B", "второй"),
        ("C", "третий"),
        ("D", "четвертый"),
        ("E", "пятый"),
        ("F", "шестой"),
    ]
    stage = models.CharField(max_length=1, choices=STAGE_CHOICES, verbose_name='Этапы лабораторного опыта/варки')
    formula = models.ForeignKey(Formula, on_delete=models.CASCADE, verbose_name='Рецептура')
    ingredient = models.ManyToManyField(Ingredient, verbose_name='Ингредиент')
    brix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Brix')
    dry_matter = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сухих веществ')
    quantity_1 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество на 1 кг продукта')
    unit_of_measure = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Единицы измерения')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    index_e = models.CharField(max_length=12, verbose_name='Е-индекс')
    level_in_total_volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Доля в общем объеме')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    def __str__(self):
        return (f'Рецептура: {self.formula},\n'
                f'Этап: {self.stage},\n'
                f'Ингредиент: {self.ingredient.name},\n'
                f'BRIX: {self.brix},\n'
                f'E index: {self.index_e},\n'
                f'Цена: {self.price}')

    def quantity_quotient(self, quotient):
        """Метод для расчета количества ингредиентов на варку 100/200/300кг варку и т.д."""
        return self.quantity_1 * quotient

    def total_sum_dry_matter(self):
        """Метод для расчета количества сухих веществ итого"""
        return sum(FormulaIngredients.dry_matter)

    def total_sum_price(self):
        """Метод для расчета себестоимости продукта"""
        return sum(FormulaIngredients.price)

    def level_in_total_volume(self):
        """Метод для расчета доли ингредиента в общей массе продукта"""
        return self.level_in_total_volume / sum(FormulaIngredients.level_in_total_volume) * 100

    class Meta:
        verbose_name = 'Ингредиент в рецептуре'
        verbose_name_plural = 'Ингредиенты в рецептуре'
