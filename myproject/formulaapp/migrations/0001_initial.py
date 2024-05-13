# Generated by Django 5.0.4 on 2024-05-13 14:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredientsapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Formula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('date_added', models.DateField(auto_now_add=True, verbose_name='Дата добавления')),
                ('recipe_status', models.CharField(choices=[('Н', 'новая'), ('Д', 'доработка'), ('У', 'утвержденная')], max_length=1)),
                ('status_success', models.CharField(choices=[('S', 'success'), ('F', 'fail')], max_length=1)),
                ('description_formula', models.TextField(verbose_name='Технологический процесс')),
                ('name_product', models.TextField(max_length=100, verbose_name='Название полученного продукта')),
                ('description_product', models.TextField(verbose_name='Описание полученного продукта')),
                ('product_photo', models.ImageField(blank=True, default='default_image.png', upload_to='myproject/media/product', verbose_name='Изображение готового продукта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рецептура',
                'verbose_name_plural': 'Рецептуры',
            },
        ),
        migrations.CreateModel(
            name='FormulaIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(choices=[('A', 'первый'), ('B', 'второй'), ('C', 'третий'), ('D', 'четвертый'), ('E', 'пятый'), ('F', 'шестой')], max_length=1, verbose_name='Этапы лабораторного опыта/варки')),
                ('brix', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Brix')),
                ('dry_matter', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сухих веществ')),
                ('quantity_1', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Количество на 1 кг продукта')),
                ('unit_of_measure', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Единицы измерения')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('index_e', models.CharField(max_length=12, verbose_name='Е-индекс')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('formula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formulaapp.formula', verbose_name='Рецептура')),
                ('ingredient', models.ManyToManyField(to='ingredientsapp.ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецептуре',
                'verbose_name_plural': 'Ингредиенты в рецептуре',
            },
        ),
    ]
