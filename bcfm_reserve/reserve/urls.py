from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from reserve.views import customer_views, admin_views

app_name = 'reserve'
urlpatterns = [
    url(r'^$', customer_views.index, name='index'),
    url(r'^login$', customer_views.login_user, name='login'),
    url(r'^logout$', customer_views.logout_user, name='logout'),
    url(r'^register$', customer_views.register, name='register'),
    url(r'^browse/$', customer_views.browse, name='browse'),
    url(r'^browse/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', customer_views.browse, name='browse'),
    url(r'^rules$', customer_views.rules, name='rules'),
    url(r'^buildings$', customer_views.buildings, name='buildings'),
    url(r'^building/(?P<building_id>[0-9]+)/$', customer_views.building_details, name='building_details'),
    url(r'^admin_building/(?P<building_id>[0-9]+)/$', admin_views.admin_building_details, name='admin_building_details'),
    url(r'^remove_contact/(?P<building_id>[0-9]+)/(?P<user_id>[0-9]+)/$', admin_views.remove_contact, name='remove_contact'),
    url(r'^space/(?P<space_id>[0-9]+)/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', customer_views.space_details, name='space'),
    url(r'^admin_space/(?P<space_id>[0-9]+)/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', admin_views.admin_space_details, name='admin_space'),
    url(r'^myaccount/(?P<user_id>[0-9]+)/$', customer_views.account, name='my_account'),
    url(r'^edit_myaccount/(?P<user_id>[0-9]+)/$', customer_views.edit_account, name='edit_account'),
    url(r'^myreservations/(?P<user_id>[0-9]+)/$', customer_views.reservation, name='reservation'),
    url(r'^delete_reservation/(?P<reservation_id>[0-9]+)/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', customer_views.delete_reservation, name='delete_reservation'),
    url(r'^admin_reservations/$', admin_views.admin_reservation, name='admin_reservation'),
    url(r'^user_permissions/$', admin_views.user_permissions, name='user_permissions'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)