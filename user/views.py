from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User
from django.utils import timezone
import string
import random


def random_str(length=6, population=string.ascii_letters):
    return "".join(random.sample(population, length))


def register(request):
    # a = request.GET["a"]
    now = timezone.now()
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    # random_str(10, population=string.printable)

    valid = True
    if not username or not password:
        valid = False

    count = User.objects.filter(username=username).count()
    if count > 0:
        valid = False

    if valid:
        new_user = User(username=username, password=password, register_time=now)
        new_user.save()
        return JsonResponse({"success": True, "username": new_user.username, "register time": new_user.register_time})
    else:
        return JsonResponse({"success": False})
