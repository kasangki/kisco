from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import TBUsers
from .forms import LoginForm
from django.core.paginator import Paginator

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user_id'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def users_list(request):
    users = TBUsers.objects.all().order_by('-user_id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(users, 20)

    users_list = paginator.get_page(page)
    return render(request, 'users_list.html', {'users_list': users_list})