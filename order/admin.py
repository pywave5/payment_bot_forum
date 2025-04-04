from django.contrib import admin
from order.models import Referral
from order.models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone_number",
        "username",
        "customer_name",
        "ticket_name",
        "total_cost",
        "payment_method",
        "is_paid"
    )
    list_filter = ("is_paid", "payment_method",)
    search_fields = ("id", "customer_name", "ticket_name", "payment_method")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "ref_code", "start", "number", "payments")
    search_fields = ("user_id", "username", "ref_code")

admin.site.register(Order, OrderAdmin)