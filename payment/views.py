import asyncio
import os
import threading
from aiogram import Bot
from asgiref.sync import sync_to_async
from payme.types import response
from payme.views import PaymeWebHookAPIView
from payme.models import PaymeTransactions
from order.models import Order, Referral
from dotenv import load_dotenv

load_dotenv()

class AsyncBotManager:
    _bot_instance = None
    _loop = None
    _thread = None

    @classmethod
    def get_bot(cls):
        if cls._bot_instance is None:
            cls._bot_instance = Bot(token=os.getenv("BOT_TOKEN"))
        return cls._bot_instance

    @classmethod
    def get_loop(cls):
        if cls._loop is None or cls._loop.is_closed():
            cls._loop = asyncio.new_event_loop()
            cls._thread = threading.Thread(target=cls._run_loop, args=(cls._loop,), daemon=True)
            cls._thread.start()
        return cls._loop

    @staticmethod
    def _run_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

class PaymeCallBackAPIView(PaymeWebHookAPIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = AsyncBotManager.get_bot()
        self.loop = AsyncBotManager.get_loop()

    def check_perform_transaction(self, params) -> response.CheckPerformTransaction:
        account = self.fetch_account(params)
        self.validate_amount(account, params.get("amount"))
        return response.CheckPerformTransaction(allow=True).as_resp()

    def handle_created_payment(self, params, result, *args, **kwargs):
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        transaction = PaymeTransactions.get_by_transaction_id(transaction_id=params["id"])
        order_id = transaction.account_id or params.get("account", {}).get("id")

        if not order_id:
            return

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return

        # Достаём реферальный код и юзернейм
        ref_code = order.ref_code if hasattr(order, "ref_code") else None
        ref_username = self.get_referral_username(ref_code) if ref_code else "Без реферала"

        order.is_paid = True
        order.save(update_fields=["is_paid"])

        if order.telegram_id:
            self._send_payment_notifications(order, ref_username)

    @sync_to_async
    def get_referral_username(self, ref_code):
        try:
            referral = Referral.objects.get(ref_code=ref_code)
            return referral.username
        except Referral.DoesNotExist:
            return "Неизвестный реферал"

    def _send_payment_notifications(self, order, ref_username):
        future = asyncio.run_coroutine_threadsafe(
            self._send_async_messages(order, ref_username), self.loop
        )
        try:
            future.result()
        except Exception as e:
            print(f"❌ Ошибка при отправке сообщений: {e}")

    async def _send_async_messages(self, order, ref_username):
        chat_id = -1002649801891
        topic_id = 6

        message = self._format_user_message(order)
        topic_message = self._format_admin_message(order, ref_username)

        try:
            await self.bot.send_message(order.telegram_id, message, parse_mode="HTML", disable_web_page_preview=True)
            await self.bot.send_message(chat_id, topic_message, message_thread_id=topic_id, parse_mode="HTML")
        except Exception as e:
            print(f"❌ Ошибка при отправке сообщений: {e}")

    def _format_user_message(self, order):
        name = "UNKNOWN"
        link = "https://t.me/nafisa_dma"
        if order.ticket_name == "standart":
            name = "STANDART"
            link = "https://t.me/+0myxWy0nhes3ZjY6"
        elif order.ticket_name == "comfort":
            name = "COMFORT"
            link = "https://t.me/+HnAhRR7OhBI4Njdi"
        elif order.ticket_name == "business":
            name = "BUSINESS"
            link = "https://t.me/+ZMXyyVSErr8zMTk6"
        elif order.ticket_name == "vip":
            name = "VIP"
            link = "https://t.me/+w9SqkzJj8pdmMDFi"
        elif order.ticket_name == "platinum":
            name = "PLATINUM"
            link = "https://t.me/+-y57CZguW8ZhNmUy"

        text = (f"Tabriklaymiz! Hayotingizni o'zgartirish yo'lidagi birinchi qadamni qo'ydingiz\n\n"
                f"GLOBAL WOMEN FORUM uchun to'lovingiz tasdiqlandi. Biletingizni olish uchun https://t.me/nafisa_dma bilan bog'lanishingizni so'rab qolamiz.\n\n"
                f"Siz {name} SEKTORIDAN bilet xarid qildingiz. Ushbu tarif qatnashchilar uchun maxsus yopiq telegram guruhga kirishingizni so'rab qolamiz zero STANDART TARIFI Bonus darsliklari aynan shu YOPIQ TELEGRAM guruhda beriladi.\n\n"
                f"Yopiq канал linki:\n"
                f"{link}\n"
                f"{link}\n"
                f"{link}\n"
                f"Hurmat bilan GLOBAL WOMEN FORUM tashkilotchilari\n"
                f"——-")

        return text

    def _format_admin_message(self, order, ref_username):
        return (f"✅ОПЛАТА\n\n"
                f"👤 Клиент - <b>{order.customer_name}</b>\n"
                f"🎫 Билет - <b>{order.ticket_name.upper()}</b>\n"
                f"💰 Сумма - <b>{order.total_cost} сум</b>\n"
                f"📞 Номер - {order.phone_number}"
                f"👥 Реферал: <b>{ref_username}</b>")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        transaction = PaymeTransactions.get_by_transaction_id(transaction_id=params["id"])

        if transaction.state == PaymeTransactions.CANCELED:
            try:
                order = Order.objects.get(id=transaction.account.id)
                order.is_paid = False
                order.save()
            except Order.DoesNotExist:
                pass