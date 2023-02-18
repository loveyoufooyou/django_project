from django.urls import re_path
from .views import LoginView, RegisterView, IndexView

urlpatterns = [
    re_path('^index/$', IndexView.as_view(), name='index'),
    re_path('^login/$', LoginView.as_view()),
    re_path('^register/$', RegisterView.as_view()),
]