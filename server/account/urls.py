from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'get_detail', views.get_detail, name='get_detail' ),

]

