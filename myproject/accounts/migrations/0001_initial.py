# Generated by Django 5.0.4 on 2024-05-13 14:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Имя пользователя')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Телефон')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='Последний вход')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Администратор')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Персонал')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Супер пользователь')),
            ],
            options={
                'verbose_name': 'Учетную запись',
                'verbose_name_plural': 'Учетные записи',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(blank=True, max_length=100, verbose_name='Адрес 1')),
                ('address_line_2', models.CharField(blank=True, max_length=100, verbose_name='Адрес 2')),
                ('profile_picture', models.ImageField(blank=True, upload_to='userprofile', verbose_name='Фото профиля')),
                ('city', models.CharField(blank=True, max_length=20, verbose_name='Город')),
                ('region', models.CharField(blank=True, max_length=20, verbose_name='Регион')),
                ('country', models.CharField(blank=True, max_length=20, verbose_name='Страна')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
    ]