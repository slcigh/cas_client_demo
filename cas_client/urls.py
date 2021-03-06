from django_cas_ng.views import login, logout, callback
from django.conf.urls import url, include
from accounts.views import index, LoginView

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^api/login$', LoginView.as_view(), name='api_login'),
    url(r'^accounts/login$', login, name='cas_ng_login'),
    url(r'^accounts/logout$', logout, name='cas_ng_logout'),
    url(r'^accounts/callback$', callback, name='cas_ng_proxy_callback'),
    url(r'^', include('accounts.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
