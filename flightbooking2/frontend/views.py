from django.shortcuts import render
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.middleware.csrf import get_token

import requests
import json



def index(request):
    url = 'http://localhost:8000/flights/'
    response = requests.get(url, cookies=request.COOKIES)
    flights = response.json()
    for flight in flights:
         # Преобразование строки в объект datetime.datetime
        flight['departure_time'] = datetime.strptime(flight['departure_time'], '%Y-%m-%dT%H:%M:%SZ')
        flight['arrival_time'] = datetime.strptime(flight['arrival_time'], '%Y-%m-%dT%H:%M:%SZ')
    return render(request, 'index.html', {'flights': flights})

def flight_detail(request, id_flight):
    current_url = request.get_full_path()
    url = f'http://localhost:8000/flights/{id_flight}/tickets/'
    response = requests.get(url, cookies=request.COOKIES)
    # print(response.json())
    tickets = response.json()['tickets']
    booking_tickets = response.json()['booking_tickets']
    booking_list = [ticket['id_ticket'] for ticket in booking_tickets]

    if request.user.is_authenticated:
        username = request.user.username
        url = f'http://localhost:8000/gateway/bookingQuotasByUser/{username}/'
        response = requests.get(url, cookies=request.COOKIES)
        try:
            json_response = response.json()
            max_quota = json_response[0]['max_quota']
            use_quota = json_response[0]['use_quota']
            rem_quota = max_quota - use_quota
        except:
            rem_quota = 5

    if request.method == 'POST':
        if request.user.is_authenticated:
            # получаем данные с формы
            selected_tickets = request.POST.getlist('selected_tickets')
            if len(selected_tickets) <= rem_quota:
                headers = request.headers
                cookies = request.COOKIES

                # Получение CSRF-токена
                csrf_token = get_token(request)

                # Включение CSRF-токена в заголовок запроса
                headers_dict = dict(headers)
                headers_dict['X-CSRFToken'] = csrf_token

                batch_data = {'flight_number': id_flight, 'tickets': [{'ticket_id': ticket_id} for ticket_id in selected_tickets]}
                json_data = json.dumps(batch_data)
                url = 'http://localhost:8000/bookings/'
                response = requests.post(url, headers=headers_dict, cookies=cookies, json=json_data)

                # Перенаправить пользователя на страницу успешного бронирования
                return redirect(current_url)
            else:
                messages.error(request, f'Вы пытаетесь забронировать билетов больше чем допустимо, для вас доступно {rem_quota} броней')
        else:
            # Если пользователь не авторизован, вывести сообщение
            messages.error(request, 'Для отправки формы необходимо авторизоваться.')

    return render(request, 'flight_detail.html', {'tickets' : tickets, 'booking_tickets' : booking_list, 'id_flight' : id_flight})


def user_page(request, username):
    username = username
    url = f'http://localhost:8000/gateway/{username}/bookingTickets/'

    headers = request.headers
    cookies = request.COOKIES
    method = request.method

    params = {
            'username' : username
        }

    if method == 'GET':

        response = requests.get(url, cookies=cookies, params = params)
        if response.status_code == 200:
            user_booking = response.json()
        else:
            user_booking = []

        for booking in user_booking:
            # Преобразование строки в объект datetime.datetime
            booking['departure_time'] = datetime.strptime(booking['departure_date'], '%Y-%m-%dT%H:%M:%SZ')
            booking['arrival_time'] = datetime.strptime(booking['arrival_date'], '%Y-%m-%dT%H:%M:%SZ')

    if method == 'POST':
        selected_tickets = request.POST.getlist('selected_tickets')
        # Получение CSRF-токена
        csrf_token = get_token(request)

        # Включение CSRF-токена в заголовок запроса
        headers_dict = dict(headers)
        headers_dict['X-CSRFToken'] = csrf_token
        batch_data = {'tickets': [{'ticket_id': ticket_id} for ticket_id in selected_tickets]}
        json_data = json.dumps(batch_data)
        url = 'http://localhost:8000/bookingTickets/'
        response = requests.post(url, headers=headers_dict, cookies=cookies, json=json_data)
        if response.ok:
            print('Получили ответ на фронтенд')
        else:
            print(f"Error sending POST request: {response.status_code}")

        user_booking = requests.get(url, cookies=cookies, params = params).json()

    return render(request, 'user_page.html', {'username': username, 'user_booking': user_booking})