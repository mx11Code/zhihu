from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User, UserForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
import string
import random
from django.core.mail import send_mail


def random_str(length=15, population=string.ascii_letters):
    return "".join(random.sample(population, length))


def register(request):
    # a = request.GET["a"]
    now = timezone.now()

    # exists_user = User.objects.get(pk=1)
    # form = UserForm(request.POST)

    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    register_email = request.POST.get("register_email", "")
    # random_str(10, population=string.printable)

    # valid = True
    # if not username or not password:
    #     valid = False
    #
    # count = User.objects.filter(username=username).count()
    # if count > 0:
    #     valid = False
    #
    # if valid:
    new_user = User(username=username, password=password, register_time=now, register_email=register_email)
    new_user.save()

    # new_user = form.save(commit=False)
    return JsonResponse(
        {"register_email": new_user.register_email, "success": True, "username": new_user.username,
         "register time": new_user.register_time})  # else:
    # return JsonResponse({"success": False})


def reset(request):
    # form = UserForm(request.POST)
    email = request.POST.get("email")
    # user_id = request.POST.get("id")

    exist_user = get_object_or_404(User, register_email=email)
    token = random_str()

    exist_user.reset_token = token
    exist_user.reset_token_time = timezone.now()
    exist_user.save()
    to_email = "492779595@qq.com"
    send_mail(
        'Verify mailbox',
        'http://127.0.0.1/user/reset/confirm/%s/%s' % (exist_user.id, token),
        '18672553257@163.com',
        [to_email],
        fail_silently=False,
    )
    return JsonResponse({"success": True})
