from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from authenticate.forms import LoginForm, RegisterForm
import requests

def login_user(request):
    context = {'login_form': LoginForm()}

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                context = {
                    'login_form': login_form,
                    'attention': f'The user {username} and password not found!'
                }
        else:
            context = {
                'login_form': login_form,
            }

    return render(request, 'auth/login.html', context)


class RegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get(self, request):
        user_form = RegisterForm()
        context = {"user_form": user_form}
        return render(request, 'auth/register.html', context)

    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

                # Создадим квоту для нового пользователя
            url = 'http://localhost:8000/api/bookingQuotas/'
            # Данные пользователя
            username = user_form.cleaned_data['username']
            max_quota = 5
            use_quota = 0

            # Параметры запроса
            data = {
                'username': username,
                'max_quota': max_quota,
                'use_quota': use_quota
            }
            # Отправка POST-запроса
            print('Отправляем запрос на создание квоты')
            response = requests.post(url, data=data)
            # Проверка статуса ответа
            if response.status_code == 201:
                print('Запрос на добавление квоты успешно обработан')
            else:
                print('Ошибка при обработке запроса на добавление квоты:', response.status_code)

            login(request, user)
            return redirect('index')

        context = {"user_form": user_form}
        return render(request, 'auth/register.html', context)

def logout_user(request):
    logout(request)
    return redirect('index')
