from django_cas_ng.backends import CASBackend
from django_cas_ng.utils import get_cas_client
from django.conf import settings
from django.contrib.auth.models import User
from django_cas_ng.signals import cas_user_authenticated
from accounts.models import UserInfo


class CustomCASBackend(CASBackend):
    def authenticate(self, ticket, service, request):
        """Verifies CAS ticket and gets or creates User object"""
        client = get_cas_client(service_url=service)
        username, attributes, pgtiou = client.verify_ticket(ticket)
        if attributes:
            request.session['attributes'] = attributes
        if not username:
            return None

        try:
            user = User.objects.get(**{User.USERNAME_FIELD: username})
            created = False
        except User.DoesNotExist:
            # check if we want to create new users, if we don't fail auth
            if not settings.CAS_CREATE_USER:
                return None
            # user will have an "unusable" password
            user = User.objects.create_user(username, '')
            user.save()
            ui = UserInfo()
            ui.user = user
            ui.nickname = "test"
            ui.save()
            created = True

        if not self.user_can_authenticate(user):
            return None

        if pgtiou and settings.CAS_PROXY_CALLBACK:
            request.session['pgtiou'] = pgtiou

        # send the `cas_user_authenticated` signal
        cas_user_authenticated.send(
            sender=self,
            user=user,
            created=created,
            attributes=attributes,
            ticket=ticket,
            service=service,
        )
        return user

    def user_can_authenticate(self, user):
        return True

    def get_user(self, user_id):
        """Retrieve the user's entry in the User model if it exists"""

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
