from django.shortcuts import render, redirect, get_object_or_404
from .models import Aircraft, Flight_list, Flight_detail, Booking_quota, User_lock_tickets
from django.utils.http import urlencode
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import CustomUserCreationForm, PathDateForm
from django.db.models import Q
from datetime import datetime, timedelta

def index(request): #Обработка главной страницы
    if request.method == 'POST': # эта часть не работает, сразу запускаеться блок ealse а рендер идет через форму action
        form = PathDateForm(request.POST)
        if form.is_valid():
            context = {
            'first_date' : form.cleaned_data['first_date'],
            'second_date' : form.cleaned_data['second_date'],
            'from_country' : form.cleaned_data['from_country'],
            'to_country' : form.cleaned_data['to_country'],
            }
            # url = reverse('flight_list') + '?' + urlencode(context) # не сработало
            # Обработка данных из формы
            return redirect('flight_list', context) # перенаправление на новую страницу
    else:
        form = PathDateForm(
            initial={
                'first_date':'2021-01-01',
                'second_date':'2021-01-01',
                'from_country':'Russia',
                'to_country':'Turkey'
            }
        )
    context = {'form': form}
    return render(request, 'index.html', context)

def flight_list(request):
    from_country = request.POST.get('from_country')
    to_country = request.POST.get('to_country')
    first_date = datetime.strptime(request.POST.get('first_date'), '%Y-%m-%d')
    second_date = datetime.strptime(request.POST.get('second_date'), '%Y-%m-%d')

    flights = Flight_list.objects.filter(
        Q(country_source=from_country) &
        Q(country_target=to_country) &
        Q(departure_time__range=(first_date.date(), second_date.date() + timedelta(days=1))) &
        Q(arrival_time__range=(first_date.date(), second_date.date() + timedelta(days=1)))
    )
    context = {
        'flights': flights
    }
    return render(request, 'flight_list.html', context)

def flight_detail(request, number_flight):
    if request.method == 'POST':
        id_tickets_true = request.POST.getlist('ticket_ids')
        # Обновляем данные в базе данных
        Flight_detail.objects.filter(id_ticket__in=id_tickets_true).update(username=request.user.username)
        # Получаем объект модели Booking_quota для текущего пользователя
        booking_quota = get_object_or_404(Booking_quota, username=request.user.username)

        # Обновляем поле use_quota в объекте модели Booking_quota
        booking_quota.use_quota += len(id_tickets_true)
        booking_quota.save()

        country_source = request.POST.get('country_source', '')
        country_target = request.POST.get('country_target', '')
    else:
        country_source = ''
        country_target = ''

    tickets = Flight_detail.objects.filter(
        Q(id_flight=number_flight)
    )
    booking_quota = get_object_or_404(Booking_quota, username=request.user.username)
    free_count_quota = booking_quota.all_quota - booking_quota.use_quota
    sorted_tickets = sorted(tickets, key=lambda x: x.seat_number)


    context = {
        'tickets': sorted_tickets,
        'free_count_quota': free_count_quota,
        'country_source': country_source,
        'country_target': country_target
        }
    return render(request, 'flight_detail.html', context)

def login_view(request): # Обработка формы авторизации
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})


def registration_view(request): # Обработка регистрации
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})


def information(request):
    return render(request, 'information.html')


def personal(request):
    if request.method == 'POST':
        tickets_cansell = request.POST.getlist('ticket_lock')
        total_tickets = int(request.POST.get('total_tickets'))
        print(tickets_cansell)
        print(total_tickets)

        # Обновляем данные в базе
        Flight_detail.objects.filter(id_ticket__in=tickets_cansell).update(username=None)
        Booking_quota.objects.filter(username = request.user.username).update(use_quota = int(total_tickets) - len(tickets_cansell))

    user_lock_tickets = User_lock_tickets.objects.filter(username = request.user.username)
    context = {
        'user_lock_tickets': user_lock_tickets
    }
    return render(request, 'personal.html', context)