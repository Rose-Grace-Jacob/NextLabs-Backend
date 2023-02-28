from django.urls import include, path
from .views import *

urlpatterns = [
    path('register/', SignupView.as_view()),
    path('userprofile/', UserProfile.as_view()),
    path('usertasks/', UserTask.as_view()),
    path('showapps/',Showapp.as_view()),
    path('completetask/',Completetask.as_view()),
    path('addapps/', Addapp.as_view()),
    path('adminapps/', Adminapps.as_view()),
]