from django.conf.urls import url
from . import views

urlpatterns = [
            url(r'getMatchInfo', views.getMatchInfo, name='getMatchInfo' ),
            url(r'createBill', views.createBill, name='createBill' ),
            url(r'getFootballBills', views.getFootballBills, name='getFootballBills' ),
            url(r'getFootballBillDetail', views.getFootballBillDetail, name='getFootballBillDetail' ),
            url(r'payFootball', views.payFootball, name='payFootball' ),
            url(r'delFootballBill', views.delFootballBill, name='delFootballBill' ),

            url(r'getTraditionalInfo', views.getTraditionalInfo, name='getTraditionalInfo' ),
            url(r'createTraditionalBill', views.createTraditionalBill, name='createTraditionaleBill' ),

]

