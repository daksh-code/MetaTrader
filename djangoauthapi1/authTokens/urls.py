from django.urls import path
from .views import AuthTokenView
urlpatterns = [
    path('authtokens/', AuthTokenView.as_view(), name='authtokens'),
    
]