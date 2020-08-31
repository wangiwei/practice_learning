from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse

from read_statistics.utils import get_seven_days_read_data, get_today_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取热门博客缓存
    today_hot_data = cache.get('today_hot_data')
    if today_hot_data is None:
        today_hot_data = get_today_hot_data(blog_content_type)
        cache.set('today_hot_data', today_hot_data, 3600)
        # print('cal')
    else:
        # print('use cache')
        pass

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    return render(request, 'home.html', context)

def login_(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
