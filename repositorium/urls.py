from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    #Console routes
    url(r'^$', 'users.views.create_user'),
    url(r'^home/','console.views.home'),
    url(r'^app/create/','console.views.create_app'),

    #Api routes
    url(r'^api/v1.0/users/punctuation/$','users.views.get_punctuation'),
    url(r'^api/v1.0/apps/$','core.views.create_app'),
    url(r'^api/v1.0/criteria/$','core.views.create_criterion'),
    url(r'^api/v1.0/documents/$','documents.views.create_document'),
    
    #Oauth routes

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^users/login/$', 'users.views.log_in'),
    url(r'^users/logout/$','django.contrib.auth.views.logout',{'next_page' : '/'}),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
