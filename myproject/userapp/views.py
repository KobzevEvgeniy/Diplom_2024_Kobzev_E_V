from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites import requests
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from cabinetapp.models import Cabinet, CabinetItem
from cabinetapp.views import _cabinet_id
from formulaapp.models import Formula, FormulaIngredients
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import User, UserProfile


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                            username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # CREATE USER PROFILE
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'myproject/media/user_pictures/default-user.png'
            profile.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Активируйте свой аккаунт в Technology_desktop'
            message = render_to_string('userapp/user_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/userapp/login.html/?command=verification&email=' + email)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'userapp/register.html', context)


#####

#### сюда вставить метод с кабинетом

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cabinet = Cabinet.objects.get(cabinet_id=_cabinet_id(request))
                is_cabinet_item_exists = CabinetItem.objects.filter(cabinet=cabinet).exists()
                if is_cabinet_item_exists:
                    cabinet_item = CabinetItem.objects.filter(cabinet=cabinet)

                    formula_variation = [list(item.variations.all()) for item in cabinet_item]

                    cabinet_item = CabinetItem.objects.filter(user=user)
                    existing_variation_list = [list(item.variations.all()) for item in cabinet_item]
                    item_id_list = [item.id for item in cabinet_item]

                    for prod_var in formula_variation:
                        if prod_var in existing_variation_list:
                            item_index = existing_variation_list.index(prod_var)
                            item_id = item_id_list[item_index]
                            item = CabinetItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cabinet_item = CabinetItem.objects.filter(cabinet=cabinet)
                            for item in cabinet_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'Вы вошли на сайт.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query

                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Неверные логин или пароль.')
            return redirect('login')
    return render(request, 'userapp/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Вы вышли.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Поздравляем! Ваш аккаунт активирован.')
        return redirect('login')
    else:
        messages.error(request, 'Неверная ссылка активации.')
        return redirect('register')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Сбросьте ваш пароль'
            message = render_to_string('userapp/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Письмо сброса пароля отправлено на вашу электронную почту.')
            return redirect('login')
        else:
            messages.error(request, 'Такой аккаунт не существует!')
            return redirect('forgotPassword')
    return render(request, 'userapp/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Пожалуйста, обновите свой пароль')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Срок действия данной ссылки истек!')
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Пароль успешно обновлен!')
            return redirect('login')
        else:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def dashboard(request):
    formula = Formula.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    formula_count = formula.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'formula_count': formula_count,
        'userprofile': userprofile
    }
    return render(request, 'userapp/dashboard.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был обновлен.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }
    return render(request, 'userapp/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Пароль успешно обновлен.')
                return redirect('change_password')
            else:
                messages.error(request, 'Пожалуйста, введите правильный текущий пароль.')
                return redirect('change_password')
        else:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('change_password')
    return render(request, 'userapp/change_password.html')


@login_required(login_url='login')
def my_formulas(request):
    formula = Formula.objects.get(user=request.user)
    my_formula = FormulaIngredients.objects.filter(formula.user.pk)

    sub_total_price = 0
    sub_total_brix = 0
    for i in my_formula:
        sub_total_price += i.price * i.quantity_1
        sub_total_brix += i.brix * i.quantity_1

    context = {
        'my_formula': my_formula,
        'formula': formula,
        'date_added': formula.date_added,
        'name_product': formula.ame_product,
        'sub_total_price': sub_total_price,
        'sub_total_brix': sub_total_brix,
        'stage': formula.stage,
        'status_success': formula.status_success

    }
    return render(request, 'userapp/my_formulas.html', context)


@login_required(login_url='login')
def formula_detail(request, formula_id):
    formula = Formula.objects.get(formula_id=formula_id)
    formula_details = FormulaIngredients.objects.filter(formula_id=formula_id)

    sub_total_price = 0
    sub_total_brix = 0
    sub_level_in_total_volume = 0

    for i in formula_details:
        sub_total_price += i.price * i.quantity_1
        sub_total_brix += i.brix * i.quantity_1
        sub_level_in_total_volume += i.level_in_total_volume

    context = {
        'full_name': formula.full_name,
        'recipe_status': formula.recipe_status,
        'date_added': formula.date_added,
        'name_product': formula.name_product,
        'status_success': formula.status_success,
        'stage': formula_details.ingredient.stage,
        'ingredient': formula_details.ingredient.name,
        'BRIX': formula_details.ingredient.brix,
        'sub_total_brix': sub_total_brix,
        'quantity_1': formula_detail.ingredient.quantity_1,
        'unit_of_measure': formula_details.ingredient.unit_of_measure,
        'price': formula_detail.ingredient.price,
        'level_in_total_volume': formula_details.ingredient.level_in_total_volume,
        'sub_level_in_total_volume': sub_level_in_total_volume,
        'sub_total_price': sub_total_price,
        'description_formula': formula.description_formula,
        'description_product': formula.description_product

    }
    return render(request, 'userapp/formula_detail', context)
