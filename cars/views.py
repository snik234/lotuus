from django.shortcuts import render
from .models import Car
from django.shortcuts import render, get_object_or_404
from .models import Profile
from .forms import RegisterForm
from django.shortcuts import redirect
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from .forms import CarForm, MultipleImageForm
from .models import CarImage

def home(request):
    cars = Car.objects.order_by('-id')[:3]

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        car_title = request.POST.get('car_title')

        TOKEN = "8534272227:AAFsfv9AfyjY6A5dZztmImpBFskilCyNaqg"
        CHAT_ID = "5759586456"

        text_message = (
            f"*Швидке замовлення* \n\n"
            f"*Модель:* {car_title}\n"
            f"*Ім'я:* {name}\n"
            f"*Телефон:* {phone}\n"
            f"*Комментар:* {message}"
        )

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text_message,
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException:
            pass

        messages.success(request, f'Дякуємо, {name}! Вашу заявку на {car_title} успішно надіслано.')
        return redirect('/')

    return render(request, 'home.html', {'cars': cars})

def car_list(request):
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'car_list.html', {"cars": cars})


def car_detail(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        TOKEN = "8534272227:AAFsfv9AfyjY6A5dZztmImpBFskilCyNaqg"
        CHAT_ID = "5759586456"

        try:
            tg_user = car.owner.profile.telegram_username
            seller_tg = f"@{tg_user}" if tg_user else car.owner.username
        except Exception:
            seller_tg = car.owner.username

        text_message = (
            f" *Замовлення дзвінка* \n\n"
            f" *Автомобіль:* {car.title}\n"
            f" *Продавець:* {car.owner.username}\n"
            f" *Покупець:* {name}\n"
            f" *Телефон:* {phone}\n"
            f" *Коментар:* {message}"
        )

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text_message,
            "parse_mode": "Markdown"
        }

        try:
            requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException:
            pass

        messages.success(request, f'Дякуємо, {name}! Вашу заявку на Lotus успішно надіслано.')
        return redirect(f'/cars/{id}/')

    return render(request, 'car_detail.html', {'car': car})


def test_drive(request):
    cars = Car.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        car_title = request.POST.get('car_title')
        date = request.POST.get('date')
        time = request.POST.get('time')

        TOKEN = "8534272227:AAFsfv9AfyjY6A5dZztmImpBFskilCyNaqg"
        CHAT_ID = "5759586456"

        text_message = (
            f"🏎 *Запис на мест-драйв* 🏎️\n\n"
            f" *Модель:* {car_title}\n"
            f" *Дата:* {date}\n"
            f" *Час:* {time}\n"
            f" *И'мя клієнта:* {name}\n"
            f" *Телефон:* {phone}"
        )

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text_message,
            "parse_mode": "Markdown"
        }

        try:
            requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException:
            pass

        messages.success(request, f'Дякуємо, {name}! Ви успішно записалися на тест-драйв {car_title}.')
        return redirect('/test-drive/')

    return render(request, 'test_drive.html', {"cars": cars})


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            form.save()
            return redirect('/profile/')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'profile.html', {
        'profile': profile,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Реєстрація успішна! Увійдіть у свій акаунт.')
            return redirect('/accounts/login/')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })

def edit_profile(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user
        )

        if form.is_valid():

            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            form.save()
            messages.success(request, 'Профіль успішно оновлено!')
            return redirect('/profile/')

    else:

        form = ProfileForm(
            instance=profile,
            user=request.user
        )

    return render(request, 'edit_profile.html', {
        'form': form
    })


@login_required
def add_car(request):
    if request.method == 'POST':
        car_form = CarForm(request.POST, request.FILES)
        image_form = MultipleImageForm(request.POST, request.FILES)

        files = request.FILES.getlist('images')

        if car_form.is_valid() and image_form.is_valid():
            car = car_form.save(commit=False)
            car.owner = request.user
            car.save()
            for f in files:
                CarImage.objects.create(car=car, image=f)

            messages.success(request, f'Автомобіль {car.title} Успішно додано та опубліковано!')
            return redirect('/cars/')
    else:
        car_form = CarForm()

    return render(request, 'add_car.html', {'car_form': car_form})

def heritage(request):
    return render(request, 'heritage.html')


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.user.is_staff:
        car.delete()

    return redirect('/')