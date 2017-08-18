import random
import string
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Question, Comment
from user.models import User


def random_str(length=15, population=string.ascii_letters):
    return "".join(random.sample(population, length))


def create_question(request):
    title = request.POST.get("title", "")
    content = request.POST.get("content", "")
    user_id = request.POST.get("user_id", "")

    user = User.objects.get(pk=user_id)
    question = Question(title=title, content=content, user=user)
    question.save()
    return {}


def delete_question(request, pk):
    Question.objects.get(pk=pk).delete()
    return JsonResponse({"success": True})


def create_comment(request):
    content = request.POST.get("content", "")
    user_id = request.POST.get("user_id", "")

    user = User.objects.get(pk=user_id)
    comment = Comment(content=content, user=user)
    comment.save()
    return {}


def delete_comment(request, pk):
    Comment.objects.get(pk=pk).delete()
    return JsonResponse({"success": True})


def batch_create_questions(request, number):
    for i in range(int(number)):
        question = Question(title=random_str(10, population=string.ascii_lowercase),
                            content=random_str(20, population=string.ascii_lowercase),
                            user_id=random.randint(0, 50)
                            )
        question.save()


def batch_create_comments(request, number):
    for i in range(int(number)):
        comment = Comment(
            content=random_str(20, population=string.ascii_lowercase),
            user_id=random.randint(0, 50),
            question_id=random.randint(0, 50),
        )
        comment.save()
