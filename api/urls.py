from django.urls import path
from .views import SignUpUser,SignInUser

urlpatterns = [
    path('sign-up/',SignUpUser.as_view()),
    path('sign-in/',SignInUser.as_view()),
    
]
