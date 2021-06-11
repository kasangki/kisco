from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import TBUsers
from .forms import LoginForm
from django.core.paginator import Paginator
from django.http import Http404

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

#
# def login_01(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             request.session['user_id'] = form.user_id
#             return redirect('/')
#     else:
#         form = LoginForm()
#
#     return render(request, 'login-1.html', {'form': form})


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/users/login')

def users_list(request):
    users = TBUsers.objects.all().order_by('-user_id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(users, 20)

    users_list = paginator.get_page(page)
    return render(request, 'users_list.html', {'users_list': users_list})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    elif request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        user_name = request.POST.get('user_name', None)
        email_addr = request.POST.get('email_addr', None)
        position_name = request.POST.get('position_name', None)
        phone_number = request.POST.get('phone_number', None)
        user_level = request.POST.get('user_level', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)
        create_id = request.session['user_id']

        res_data = {}

        if not (user_id and user_name and email_addr and position_name and user_level and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            user = TBUsers(
                user_id=user_id,
                password=password,
                user_name=user_name,
                email_addr=email_addr,
                position_name=position_name,
                phone_number=phone_number,
                user_level=user_level,
                create_id=create_id,
                update_id=create_id
            )

            user.save()

        return redirect('/users/user_list')




def user_detail(request, pk):

    try:
        user = TBUsers.objects.get(pk=pk)
    except TBUsers.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'user_detail.html', {'user': user})

def user_update(request):

    user_id = request.POST.get('user_id', None)
    user_name = request.POST.get('user_name', None)
    email_addr = request.POST.get('email_addr', None)
    position_name = request.POST.get('position_name', None)
    phone_number = request.POST.get('phone_number', None)
    user_level = request.POST.get('user_level', None)
    password = request.POST.get('password', None)
    re_password = request.POST.get('re-password', None)
    create_id = request.session['user_id']

    res_data = {}

    if not (user_id and user_name and email_addr and position_name and user_level and password and re_password):
        res_data['error'] = '모든 값을 입력해야합니다.'
    elif password != re_password:
        res_data['error'] = '비밀번호가 다릅니다.'
    else:
        user = TBUsers(
            user_id=user_id,
            password=password,
            user_name=user_name,
            email_addr=email_addr,
            position_name=position_name,
            phone_number=phone_number,
            user_level=user_level,
            create_id=create_id,
            update_id=create_id
        )

        user.save()

    return redirect('/users/user_list')

def user_delete(request,pk):

    TBUsers.objects.get(pk=pk).delete()

    return redirect('/users/user_list')