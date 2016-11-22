from rest_framework import generics
from serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
import requests
from django.conf import settings
from django_cas_ng.utils import get_service_url
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import View
from django.http import HttpResponseRedirect


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def index(request):
    result = {}
    if request.user.is_anonymous():
        result["user"] = None
    else:
        result["user"] = request.user.username
    return Response(result)


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        self.ticket = request.GET.get('ticket')
        self.service = get_service_url(request)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.ticket:
            user = authenticate(self.ticket, self.service, request)
            if not user:
                # should 302 to seerver/login
                return HttpResponseRedirect('api_login')
            login(request, user)
            return HttpResponseRedirect('index')
        else:
            return HttpResponseRedirect('api_login')

    def post(self, request, *args, **kwargs):
        username, password = request.POST.get('username'), request.POST.get('password')
        server_url = settings.CAS_SERVER_URL
        URL = server_url + "?service=" + self.service
        client = requests.session()
        client.get(URL)
        csrftoken = client.cookies['csrf']
        authdata = {"username": username, "password": password, "csrfmiddlewaretoken": csrftoken}
        requests.post(URL, data=authdata)
