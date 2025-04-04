from django.db import models

class Referral(models.Model):
    user_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    ref_code = models.CharField(max_length=20, unique=True)
    start = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    payments = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username or self.user_id} ({self.ref_code})"

class Order(models.Model):
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    customer_name = models.CharField(max_length=255)
    ticket_name = models.CharField(max_length=255)
    total_cost = models.IntegerField()
    payment_method = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
