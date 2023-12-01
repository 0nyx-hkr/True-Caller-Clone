
from django.urls import path
from .views import register_user, login_user,mark_as_spam,search

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('spam/',mark_as_spam),
    path('search/',search),

]
