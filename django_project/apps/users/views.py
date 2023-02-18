from django.db import DatabaseError
from django.http import (
    HttpResponseForbidden, 
    HttpResponseServerError
)
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, authenticate
from django.urls import reverse

from .models import Users
# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'users/index.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        data = request.POST
        username = data.get('username', None)
        password = data.get('password', None)
        if not all([username, password]):
            return HttpResponseForbidden('请输入完整')
        user = authenticate(username=username, password=password)  # django内部的验证是拿usename
        if user is None:
            return render(request,'users/login.html', {'error': '密码错误'})

        #4、状态保持
        login(request, user)
        return redirect(reverse('users:index'))

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        data = request.POST
        username = data.get('username', None)
        phone = data.get('phone', None)
        password = data.get('password', None)
        if not all([username, phone, password]):
            return HttpResponseForbidden('请输入完整')
        if Users.objects.filter(username=username) or Users.objects.filter(phone=phone):
            return HttpResponseForbidden('手机号或昵称已被注册，请使用其他手机号')
        try:
            user = Users.objects.create_user(username=username, password=password, phone=phone)
        except DatabaseError as e:
            return HttpResponseServerError('服务器出错，注册失败')
        login(request, user)
        return redirect(reverse('users:index'))
