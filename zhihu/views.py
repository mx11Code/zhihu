from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from question.models import Question, Answer, Comment
from user.models import User
from zhihu.models import get_model_list, base_model_delete


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


def data(request):
    return JsonResponse({})


def model_list(request, model_name, page=1, page_size=20):
    model_map = {
        "user": User, "question": Question, "answer": Answer, "comment": Comment
    }
    if model_name not in model_map:
        return {'http_status_code': 404}
    model = model_map.get(model_name)
    data, count = get_model_list(request, model, page, page_size)
    return {
        "data": [m.to_dict() for m in data],
        "currentPage": int(page),
        "pageSize": int(page_size),
        "count": count
    }


def model_delete(request, model_name, pk):
    model_map = {
        "user": User, "question": Question, "answer": Answer, "comment": Comment
    }
    if model_name not in model_map:
        return {'http_status_code': 404}
    model = model_map.get(model_name)
    return base_model_delete(request, model, pk)
