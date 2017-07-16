from django.http import HttpResponse
from django.utils import timezone


def hello_world(request):
    return HttpResponse(123)


def current_time(request):
    now = timezone.now()
    html = "It is now %s." % now
    return HttpResponse(html)


def date_time(request, datetime):
    datetime = timezone.now()
    return HttpResponse(datetime)

    # def date_time_now(request):
    #     datetime = request.GET.get("")
