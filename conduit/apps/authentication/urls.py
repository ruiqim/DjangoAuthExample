from django.conf.urls import urls
from .views import RegistrationAPIView

urlpatterns = [
    url(r'^urls/?$', RegistrationAPIView.as_view()),
]
