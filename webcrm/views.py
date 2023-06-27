from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы залогинились")
            return redirect('home')
        else:
            messages.warning(request, "Произошла ошибка")
            return redirect('home')
    else:
        return render(request, 'home.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Вы разлогинились ')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # если форма валидна то с разу его логинем
            user = authenticate(username=username, password=password)
            login(request, user)
            # выводим сообщение о успешной регестрации
            messages.success(request, "Вы залогинились")
            # перенаправляем на домашнею страницу
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')

    return render(request, 'register.html', {'form': form})


