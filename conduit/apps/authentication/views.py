from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer

class RegistrationAPIView(APIView):
    # Allow any user (Authenticated or not) to hit endpoint

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user',{})

        # The create serializer, validate serializer, save serialzer pattern
        # is common

        serializer = self.serializer_class(data=user)
        serialzer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serialzer.data, status=status.HTTP_201_CREATED)
