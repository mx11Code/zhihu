import string
import random
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate as django_authenticate, login as django_login, logout as django_logout
from django.utils import timezone
from django.core.mail import send_mail

from zhihu.models import get_model_list
from .models import User


def authenticate(**kwargs):
    user = django_authenticate(**kwargs)
    if not user.is_active or user.is_deleted:
        return None
    return user


def register(request):
    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    new_user = User(email=email, password=make_password(password))
    new_user.save()
    return JsonResponse({"success": True, "id": new_user.id})


def login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    exist_user = authenticate(email=email, password=password)

    if exist_user is not None:
        django_login(request, exist_user)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": "invalid login"})


def logout(request):
    django_logout(request)
    return JsonResponse({"success": True})


def random_str(length=15, population=string.ascii_letters):
    return "".join(random.sample(population, length))


def reset(request):
    email = request.POST.get("email")
    exist_user = get_object_or_404(User, email=email)
    reset_token = random_str()
    reset_token_time = timezone.now()
    exist_user.reset_token = reset_token
    exist_user.reset_token_time = reset_token_time
    exist_user.save()
    from_email = '18672553257@163.com'
    to_emails = ['492779595@qq.com']
    send_mail('verify your mailbox', 'http://127.0.0.1:8000/users/reset/%s/%s/' % (exist_user.id, reset_token),
              from_email, to_emails, fail_silently=False)
    return JsonResponse({"success": True})


def get(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except Exception as e:
        return {"success": False}
        # return JsonResponse({"success": False}, status=404)
    # return JsonResponse(user.to_dict())
    return user.to_dict()


def user_list(request, page, page_size):
    users, count = get_model_list(request, User, page, page_size)
    return {
        "data": [user.to_dict() for user in users],
        "currentPage": int(page),
        "pageSize": int(page_size),
        "count": count
    }


def batch_create_users(request, number):
    for i in range(int(number)):
        user = User(
            email="{}@{}.com".format(random_str(10, string.ascii_letters), random_str(3, string.ascii_lowercase)),
            password=make_password(random_str(5))
        )
        user.save()
