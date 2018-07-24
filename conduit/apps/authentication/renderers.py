import json

from rest_framework.renderers import JSONRenderer

class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If `token` key is part of the response, it will be
        # a byte object. Byte objects don't serialzer well
        # Must decode before rendering User object

        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            # As mentioned, decode `token` if it is of type bytes
            data['token'] = token.decode('utf-8')


        # Finally, render data under user

        return json.dumps({
            'user': data
        })
