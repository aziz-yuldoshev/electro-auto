from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Car, Brand, Category, Favorite, TestDrive
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import OrderForm


def home(request):
    featured_cars = (
        Car.objects
        .select_related('brand', 'category')
        .filter(status='available')
        .order_by('-created_at')[:6]
    )

    brands = Brand.objects.filter(is_active=True).order_by('name')

    return render(request, 'cars/home.html', {
        'featured_cars': featured_cars,
        'brands': brands,
    })


def car_list(request):
    cars = (
        Car.objects
        .select_related('brand', 'category')
        .all()
    )

    # =========================
    # SEARCH
    # =========================

    search = request.GET.get('search', '').strip()

    if search:
        cars = cars.filter(
            Q(model__icontains=search) |
            Q(brand__name__icontains=search) |
            Q(category__name__icontains=search)
        )

    # =========================
    # BRAND FILTER
    # =========================

    brand_id = request.GET.get('brand', '')

    if brand_id:
        cars = cars.filter(brand_id=brand_id)

    # =========================
    # CATEGORY FILTER
    # =========================

    category_id = request.GET.get('category', '')

    if category_id:
        cars = cars.filter(category_id=category_id)

    # =========================
    # PRICE FILTER
    # =========================

    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    # =========================
    # RANGE FILTER
    # =========================

    min_range = request.GET.get('min_range', '')
    max_range = request.GET.get('max_range', '')

    if min_range:
        cars = cars.filter(range_km__gte=min_range)

    if max_range:
        cars = cars.filter(range_km__lte=max_range)

    # =========================
    # YEAR FILTER
    # =========================

    min_year = request.GET.get('min_year', '')
    max_year = request.GET.get('max_year', '')

    if min_year:
        cars = cars.filter(year__gte=min_year)

    if max_year:
        cars = cars.filter(year__lte=max_year)

    # =========================
    # SORTING
    # =========================

    sort = request.GET.get('sort', 'newest')

    if sort == 'price_low':
        cars = cars.order_by('price')

    elif sort == 'price_high':
        cars = cars.order_by('-price')

    elif sort == 'range_high':
        cars = cars.order_by('-range_km')

    elif sort == 'power_high':
        cars = cars.order_by('-power_hp')

    else:
        cars = cars.order_by('-created_at')

    # =========================
    # FILTER DATA
    # =========================

    brands = Brand.objects.filter(
        is_active=True
    ).order_by('name')

    categories = Category.objects.filter(
        is_active=True
    ).order_by('name')

    context = {
        'cars': cars,
        'brands': brands,
        'categories': categories,

        'search': search,
        'selected_brand': brand_id,
        'selected_category': category_id,

        'min_price': min_price,
        'max_price': max_price,

        'min_range': min_range,
        'max_range': max_range,

        'min_year': min_year,
        'max_year': max_year,

        'sort': sort,
    }

    return render(
        request,
        'cars/car_list.html',
        context
    )


from django.shortcuts import render, get_object_or_404


def car_detail(request, pk):
    car = get_object_or_404(
        Car.objects.select_related('brand', 'category'),
        pk=pk
    )

    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            car=car
        ).exists()

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'is_favorite': is_favorite,
    })


def toggle_favorite(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if not request.user.is_authenticated:
        return redirect('login')

    favorite = Favorite.objects.filter(
        user=request.user,
        car=car
    ).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            car=car
        )

    return redirect('car_detail', pk=car.pk)


def favorites(request):
    if not request.user.is_authenticated:
        return redirect('login')

    favorite_cars = (
        Favorite.objects
        .filter(user=request.user)
        .select_related('car', 'car__brand', 'car__category')
    )

    return render(request, 'cars/favorites.html', {
        'favorite_cars': favorite_cars,
    })


# =========================================================
# ⚖️ COMPARE
# =========================================================

def add_compare(request, pk):
    car = get_object_or_404(Car, pk=pk)

    compare_cars = request.session.get('compare_cars', [])

    if pk not in compare_cars:
        if len(compare_cars) >= 4:
            compare_cars = compare_cars[-3:]

        compare_cars.append(pk)

    request.session['compare_cars'] = compare_cars
    request.session.modified = True

    return redirect('car_detail', pk=pk)


def remove_compare(request, pk):
    compare_cars = request.session.get('compare_cars', [])

    if pk in compare_cars:
        compare_cars.remove(pk)

    request.session['compare_cars'] = compare_cars
    request.session.modified = True

    return redirect('compare')


def compare(request):
    compare_ids = request.session.get('compare_cars', [])

    cars = Car.objects.select_related(
        'brand',
        'category'
    ).filter(
        id__in=compare_ids
    )

    # Tanlangan mashinalar session'dagi tartibda chiqadi
    cars_dict = {car.id: car for car in cars}

    compare_cars = [
        cars_dict[car_id]
        for car_id in compare_ids
        if car_id in cars_dict
    ]

    return render(request, 'cars/compare.html', {
        'compare_cars': compare_cars,
    })


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'Tizimga muvaffaqiyatli kirdingiz!')
            return redirect('home')

        messages.error(request, 'Login yoki parol noto‘g‘ri.')

    return render(request, 'cars/login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not password:
            messages.error(request, 'Login va parolni kiriting.')
            return render(request, 'cars/register.html')

        if password != password2:
            messages.error(request, 'Parollar bir xil emas.')
            return render(request, 'cars/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu login allaqachon mavjud.')
            return render(request, 'cars/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        messages.success(
            request,
            'Hisobingiz muvaffaqiyatli yaratildi!'
        )

        return redirect('home')

    return render(request, 'cars/register.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz.')
    return redirect('home')


def test_drive(request, pk):
    car = get_object_or_404(
        Car.objects.select_related('brand', 'category'),
        pk=pk
    )

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        message = request.POST.get('message', '').strip()

        if not full_name or not phone or not date or not time:
            messages.error(
                request,
                'Iltimos, barcha majburiy maydonlarni to‘ldiring.'
            )

            return render(
                request,
                'cars/test_drive.html',
                {'car': car}
            )

        TestDrive.objects.create(
            car=car,
            user=request.user,
            full_name=full_name,
            phone=phone,
            date=date,
            time=time,
            message=message,
        )

        messages.success(
            request,
            'Test Drive arizangiz muvaffaqiyatli yuborildi!'
        )

        return redirect(
            'car_detail',
            pk=car.pk
        )

    return render(
        request,
        'cars/test_drive.html',
        {'car': car}
    )


def create_order(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.car = car
            order.save()

            messages.success(
                request,
                'Buyurtmangiz muvaffaqiyatli yuborildi! 🚗⚡'
            )

            return redirect('car_detail', pk=car.pk)
    else:
        form = OrderForm()

    return render(
        request,
        'cars/order_form.html',
        {
            'form': form,
            'car': car,
        }
    )


def about(request):
    return render(request, 'cars/about.html')
