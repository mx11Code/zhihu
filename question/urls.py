from django.conf.urls import *
from question import views

urlpatterns = [
    url(r'^createQuestion/$', views.create_question),
    url(r'^createComment/$', views.create_comment),
    url(r'^deleteComment/(\d+)/$', views.delete_comment),
    url(r'^deleteQuestion/(\d+)/$', views.delete_question),
    url(r'^batchCreateQuestions/(\d+)/$', views.batch_create_questions),
    url(r'^batchCreateComments/(\d+)/$', views.batch_create_comments)
]
