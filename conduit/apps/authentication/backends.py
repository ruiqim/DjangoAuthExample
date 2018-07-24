import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless whether the
        endpoint requires authentication

        `authenticate` has two possible return values:
        1) `None` - return `None` if do not wish to authenticate. Usually this
                authentication will fail. An example of this is when the request
                does not include token in headers

        2) `(user, token)` - return a user/token combination when authentication is successful

        If neither case is met, then return nothing and throw and error
        `AuthenticationFailed` exception and let DRF handle the rest
        """

        request.user = None

        # `auth_header` should be an array with two elements: 1) Name of
        # authentication header (in this case, "Token") and 2) the JWT that we
        # should authenticate against.

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) ==1:
            # Invalid token header. No credentials provided.
            return None

        elif len(auth_header) > 2:
            # Invalid token header. Token string should not contain space
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')


        if prefix.lower() != auth_header_prefix:
            # The auth header prefix is not what was expected
            return None

        # Custom checks have passed. the rest of the authentication process is
        # passed to the next method

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self,request,token):
        """
        Try to authenticate the given credentials. If authentication is
        successful, return the user and toke. If not, throw and error
        """

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return(user, token)
