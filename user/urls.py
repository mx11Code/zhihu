from django.conf.urls import *
from user import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(\d+)/$', views.get),
    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^reset/$', views.reset, name="reset"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^get/(\d+)/$', views.get),
    url(r'^list/(\d+)/(\d+)/$', views.user_list),
    url(r'^batchCreate/(\d+)/$', views.batch_create_users),
]
