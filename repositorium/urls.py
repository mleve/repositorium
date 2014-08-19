from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'repositorium.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^home/','console.views.home'),
    url(r'^api/v1.0/users/login/','users.views.login'),
    url(r'^api/v1.0/users/punctuation/$','users.views.get_punctuation'),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
