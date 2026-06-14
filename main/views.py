# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from .models import (Tovar, TipTovara, Kategoriya, Postavschik, Proizvoditel,
                     Zakaz, User, PunktVydachi, StatusZakaza)

# Проверка ролей
def is_admin(user):
    return user.rol == 'admin'

def is_manager_or_admin(user):
    return user.rol in ['manager', 'admin']

# Контекст для формы товара (справочники)
def form_context():
    return {
        'tipy': TipTovara.objects.all(),
        'kategorii': Kategoriya.objects.all(),
        'postavshchiki': Postavschik.objects.all(),
        'proizvoditeli': Proizvoditel.objects.all(),
    }

# Данные товара из POST
def get_tovar_data(request):
    data = {
        'artikul': request.POST['artikul'],
        'tip_tovara_id': int(request.POST['tip_tovara']),
        'tsena': float(request.POST['tsena']),
        'postavschik_id': int(request.POST['postavschik']),
        'proizvoditel_id': int(request.POST['proizvoditel']),
        'kategoriya_id': int(request.POST['kategoriya']),
        'skidka': int(request.POST['skidka']),
        'ostatok': int(request.POST['ostatok']),
        'opisanie': request.POST.get('opisanie', ''),
    }
    foto = request.FILES.get('foto')  # файл фото
    if foto:
        data['foto'] = foto
    return data

# Данные заказа из POST
def get_order_data(request):
    return {
        'polzovatel_id': int(request.POST['polzovatel']),
        'punkt_vydachi_id': int(request.POST['punkt_vydachi']),
        'data_zakaza': request.POST['data_zakaza'],
        'data_dostavki': request.POST['data_dostavki'],
        'kod_polucheniya': request.POST['kod_polucheniya'],
        'status_id': int(request.POST['status']),
    }

# Вход
def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('product_list')
    return render(request, 'login.html')

# Выход
def logout_view(request):
    logout(request)
    return redirect('product_list')

# Список товаров (все роли, поиск/фильтр/сортировка для менеджера и админа)
def product_list(request):
    products = Tovar.objects.all()
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    kategoriya = request.GET.get('kategoriya', '')
    user = request.user if request.user.is_authenticated else None

    if user and is_manager_or_admin(user):
        if search:
            products = products.filter(
                Q(artikul__icontains=search) | Q(opisanie__icontains=search) |
                Q(tip_tovara__nazvanie__icontains=search) | Q(kategoriya__nazvanie__icontains=search) |
                Q(postavschik__nazvanie__icontains=search) | Q(proizvoditel__nazvanie__icontains=search)
            )
        if kategoriya:
            products = products.filter(kategoriya_id=int(kategoriya))
        if sort == 'price_asc':
            products = products.order_by('tsena')
        elif sort == 'price_desc':
            products = products.order_by('-tsena')
        elif sort == 'qty_asc':
            products = products.order_by('ostatok')
        elif sort == 'qty_desc':
            products = products.order_by('-ostatok')

    return render(request, 'product_list.html', {
        'products': products, 'search': search, 'sort': sort,
        'kategorii': Kategoriya.objects.all(),
    })

# Добавление товара (только админ)
@user_passes_test(is_admin)
def product_add(request):
    if request.method == 'POST':
        Tovar.objects.create(**get_tovar_data(request))
        return redirect('product_list')
    return render(request, 'product_form.html', form_context())

# Редактирование товара (только админ)
@user_passes_test(is_admin)
def product_edit(request, artikul):
    tovar = get_object_or_404(Tovar, artikul=artikul)
    if request.method == 'POST':
        for field, value in get_tovar_data(request).items():
            setattr(tovar, field, value)  # обновляем каждое поле
        tovar.save()
        return redirect('product_list')
    ctx = form_context()
    ctx['tovar'] = tovar
    return render(request, 'product_form.html', ctx)

# Удаление товара (только админ)
@user_passes_test(is_admin)
def product_delete(request, artikul):
    get_object_or_404(Tovar, artikul=artikul).delete()
    return redirect('product_list')

# Список заказов (менеджер и админ)
@user_passes_test(is_manager_or_admin)
def order_list(request):
    return render(request, 'order_list.html', {'orders': Zakaz.objects.all()})

# Добавление заказа (только админ)
@user_passes_test(is_admin)
def order_add(request):
    if request.method == 'POST':
        Zakaz.objects.create(**get_order_data(request))
        return redirect('order_list')
    return render(request, 'order_form.html', {
        'polzovateli': User.objects.all(),
        'punkty': PunktVydachi.objects.all(),
        'statusy': StatusZakaza.objects.all(),
    })

# Редактирование заказа (только админ)
@user_passes_test(is_admin)
def order_edit(request, pk):
    zakaz = get_object_or_404(Zakaz, pk=pk)
    if request.method == 'POST':
        for field, value in get_order_data(request).items():
            setattr(zakaz, field, value)
        zakaz.save()
        return redirect('order_list')
    return render(request, 'order_form.html', {
        'zakaz': zakaz,
        'polzovateli': User.objects.all(),
        'punkty': PunktVydachi.objects.all(),
        'statusy': StatusZakaza.objects.all(),
    })

# Удаление заказа (только админ)
@user_passes_test(is_admin)
def order_delete(request, pk):
    get_object_or_404(Zakaz, pk=pk).delete()
    return redirect('order_list')
