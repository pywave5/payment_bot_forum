from django.utils.crypto import get_random_string
from django.http import JsonResponse
from rest_framework import views, response

from payme import Payme
from order.serializer import OrderCreateSerializer
from .models import Referral
from backend import settings

payme = Payme(payme_id=settings.PAYME_ID)

def generate_referral_link(blogger_name):
    ref_code = get_random_string(10)
    referral = Referral.objects.create(blogger_name=blogger_name, ref_code=ref_code)  # создаем объект с правильными полями
    return f"https://t.me/forum_oplata_botstart?ref={ref_code}"

def get_referral_link(request, blogger_id):
    link = generate_referral_link(blogger_id)
    return JsonResponse({"referral_link": link})

class OrderCreate(views.APIView):

    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        result = {
            "order": serializer.data
        }

        if serializer.data["payment_method"] == "payme":
            payment_link = payme.initializer.generate_pay_link(
                id=serializer.data["id"],
                amount=serializer.data["total_cost"],
                return_url="https://womenforum.uz",
            )

            result["payment_link"] = payment_link
        return response.Response(result)