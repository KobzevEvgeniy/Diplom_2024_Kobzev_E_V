from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    """class of ingredients"""

    objects = models.Manager()
    name = models.CharField(max_length=255, verbose_name='Название')
    index_e = models.CharField(max_length=12, verbose_name='Е-индекс')
    description = models.TextField(verbose_name='Описание')
    brix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество сухих веществ')
    manufacturer = models.TextField(max_length=40, verbose_name='Производитель')
    supplier = models.TextField(max_length=40, verbose_name='Поставщик')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    UNIT_OF_MEASURE_CHOICES = [
        ("л", "литр"),
        ("кг", "килограмм"),
        ("т", "тонна"),
        ("шт", "штук"),
    ]
    unit_of_measure = models.CharField(max_length=100, choices=UNIT_OF_MEASURE_CHOICES,
                                       verbose_name='Единицы измерения')
    added_date = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    image = models.ImageField(upload_to='myproject/media', default='default_image.png', blank=True,
                              verbose_name='Изображение')
    is_available = models.BooleanField(default=True, verbose_name='Доступен')

    def __str__(self):
        return (f'Название:{self.name},\n'
                f'Индекс Е:{self.index_e},\n'
                f'Описание: {self.description},\n'
                f'Производитель: {self.manufacturer},\n'
                f'Поставщик: {self.supplier},\n'
                f'Количество сухих веществ: {self.brix},\n'
                f'Стоимость: {self.price},\n'
                f'Единицы измерения: {self.unit_of_measure}')

    # def get_url(self):
    #     """
    #     Get to go to product detail page.
    #     :return: reverse url for particular product
    #     """
    #     return reverse('ingredient_detail', args=[self.name, self.image])

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class IngredientGallery(models.Model):
    objects = models.Manager()

    ingredient = models.ForeignKey(Ingredient, default=None, on_delete=models.CASCADE, verbose_name='Ингредиент')
    image = models.ImageField(upload_to='myproject/media/ingredient', max_length=255, verbose_name='Фото')

    def __str__(self):
        return self.ingredient.name


    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Галерея ингредиентов'
