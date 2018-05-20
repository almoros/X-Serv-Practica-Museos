from museos import views
from myproject import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import *

urlpatterns = [
    url(r'^usuario.css', 'museos.views.Cambio'),
	url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_URL}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logearse/', 'museos.views.logearse'),
    url(r'^login', 'museos.views.logearse'),
     url(r'^logout', 'museos.views.mylogout'),
	url(r'^museos/$', 'museos.views.museos'),
	url(r'^museos/(\d*)/$','museos.views.museos_id'),
	url(r'^about/','museos.views.about'),
    url(r'^(.*)/XML','museos.views.XML'),
	url(r'^(.*)/$','museos.views.usuario'),
	url(r'^$','museos.views.pag_ppal'),
]
