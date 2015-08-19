from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'getMatchInfo', views.getMatchInfo, name='getMatchInfo' ),

]

