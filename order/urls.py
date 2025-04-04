from django.urls import path

from order.views import OrderCreate
from order.views import get_referral_link

urlpatterns = [
    path("create/", OrderCreate.as_view()),
    path('referral_link/<int:blogger_id>/', get_referral_link, name='get_referral_link'),
]