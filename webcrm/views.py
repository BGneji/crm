from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()
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
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, 'Вы разлогинились ')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # проверка на валидность формы
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # если форма валидна, то с разу его логиним
            user = authenticate(username=username, password=password)
            login(request, user)
            # выводим сообщение об успешной регистрации
            messages.success(request, "Вы залогинились")
            # перенаправляем на домашнею страницу
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')

    return render(request, 'register.html', {'form': form})


def record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': record})
    else:
        messages.error(request, 'Вы должны залогиниться')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        del_record = Record.objects.get(id=pk)
        del_record.delete()
        messages.error(request, 'Вы удалили запись')
        return redirect('home')
    else:
        messages.error(request, 'Вы должны залогиниться')
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        # проверка на валидность формы
        if form.is_valid():
            add_record = form.save()
            messages.success(request, f'Выша запись {add_record.first_name} была добавлена ')
            return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, 'Вы должны залогиниться')
        return redirect('home')


def updated_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        # заполняем данными (instance) и подставляем вытащенный объект (record)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            updated_record = form.save()
            messages.success(request, f'Выша запись {updated_record.first_name} была изменена ')
            return redirect('home')
        return render(request, 'updated_record.html', {'form': form})
    else:
        messages.error(request, 'Вы должны залогиниться')
        return redirect('home')


