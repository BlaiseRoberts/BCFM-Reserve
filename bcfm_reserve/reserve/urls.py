from django.conf.urls import url

from . import views

app_name = 'reserve'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.logout_user, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^browse$', views.browse, name='browse'),
    url(r'^myaccount/(?P<user_id>[0-9]+)/$', views.account, name='my_account'),
    url(r'^myreservations/(?P<user_id>[0-9]+)/$', views.reservation, name='reservation'),
]