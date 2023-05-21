import requests
import json
from django.http import JsonResponse

def gateway_view(request, pk=None):
    # Получаем данные о маршруте и методе из запроса
    route = request.path_info[1:]
    method = request.method
    headers = request.headers
    response_format = '?format=json'

    headers = dict(request.headers)
    headers['Content-Type'] = 'application/json'

    try:
        url = f'http://localhost:8000/api/{route}{response_format}'
    except:
        return JsonResponse({'error': 'Unknown route'})

    if method == 'GET':
        response = requests.get(url, headers=headers, cookies=request.COOKIES)

    if method == 'POST':
        try:
            body_data = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            body_data = None
            print(f"Error decoding request body: {str(e)}")

        if body_data is not None:
            response = requests.post(url, json=body_data, headers=headers, cookies=request.COOKIES)
        else:
            return JsonResponse({'error': 'Invalid request body'})

    if response.content:
        json_response = response.json()
    else:
        json_response = {}

    # return JsonResponse(response.json(), safe=False)
    return JsonResponse(json_response, safe=False)


def gateway_view_tickets_by_flight(request, pk=None):
    id_flight = pk
    route = request.path_info[1:]
    method = request.method
    headers = request.headers
    response_format = '?format=json'
    url_tickets = f'http://localhost:8000/api/{route}{response_format}'
    url_booking = f'http://127.0.0.1:8000/api/flights/{id_flight}/bookingTickets/{response_format}'

    if method == 'GET':
        response_tickets = requests.get(url_tickets, headers=headers, cookies=request.COOKIES)
        responce_bookint_tickets = requests.get(url_booking, headers=headers, cookies=request.COOKIES)
        response = {
                    'tickets': response_tickets.json(),
                    'booking_tickets': responce_bookint_tickets.json()
                   }

    return JsonResponse(response, safe=False)


def gateway_view_booking_tickets_user(request, username):
    url = f'http://localhost:8000/api/user/{username}/bookingTickets/'
    response = requests.get(url, headers=request.headers, cookies=request.COOKIES, params=request.GET)
    return JsonResponse(response.json(), safe=False)


def gateway_view_quota(request, username=None):
    if request.method == 'GET':
        # Ваш код для отправки GET-запроса на указанный эндпоинт и получения данных
        url = f'http://localhost:8000/api/bookingQuotasByUser/{username}'
        response = requests.get(url)

        # Проверяем статус код ответа
        if response.status_code == 200:
            json_response = response.json()
            return JsonResponse(json_response, safe=False)
        else:
            return JsonResponse({'error': 'Failed to retrieve data'}, status=response.status_code)

    return JsonResponse({'error': 'Invalid request method'})

