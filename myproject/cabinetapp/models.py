from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .views import _cabinet_id
from formulaapp.models import Formula
from userapp.models import User


class Cabinet(models.Model):
    objects = models.Manager()
    cabinet_id = models.CharField(max_length=250, blank=True, verbose_name='ID кабинета')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.cabinet_id

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class CabinetItem(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    formula = models.ForeignKey(Formula, on_delete=models.CASCADE, verbose_name='Рецептура')
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE, null=True, verbose_name='Кабинет')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    def __unicode__(self):
        return self.formula

    class Meta:
        verbose_name = 'Рецептуры пользователя'
        verbose_name_plural = 'Рецептуры пользователя'


def counter(request):
    """
    Count quantity of formulas in the cabinet.
    :param request:
    :return: Count quantity of formulas in the cabinet.
    """
    cabinet_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cabinet = Cabinet.objects.filter(cabinet_id=_cabinet_id(request))
            if request.user.is_authenticated:
                cabinet_items = CabinetItem.objects.all().filter(user=request.user)
            else:
                cabinet_items = CabinetItem.objects.all().filter(cart=cabinet[:1])
            for cabinet_item in cabinet_items:
                cabinet_count += cabinet_item.quantity
        except ObjectDoesNotExist:
            cabinet_count = 0
    return dict(cabinet_count=cabinet_count)
from django.db import models

# Create your models here.
