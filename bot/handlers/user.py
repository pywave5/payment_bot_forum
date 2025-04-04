import os

from asgiref.sync import sync_to_async

from aiogram import Router, F
from aiogram.filters.command import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.keyboards.user import *
from bot.states.user_states import UserRateStates
from bot.utlis.payme_methods import create_order
from order.models import Referral

user = Router()

@sync_to_async
def get_referral_username(ref_code):
    try:
        referral = Referral.objects.get(ref_code=ref_code)
        return referral.username
    except Referral.DoesNotExist:
        return "Неизвестный реферал"

@sync_to_async
def increment_referral_start(ref_code):
    try:
        referral = Referral.objects.get(ref_code=ref_code)
        referral.start += 1
        referral.save()
    except Referral.DoesNotExist:
        print("Invalid referral code")

@sync_to_async
def increment_referral_number(ref_code):
    try:
        referral = Referral.objects.get(ref_code=ref_code)
        referral.number += 1
        referral.save()
    except Referral.DoesNotExist:
        print("Invalid referral code")

@sync_to_async
def increment_referral_payment(ref_code):
    try:
        referral = Referral.objects.get(ref_code=ref_code)
        referral.payments += 1
        referral.save()
    except Referral.DoesNotExist:
        print("Invalid referral code")

@user.message(CommandStart())
async def cmd_start_handler(message: Message, state: FSMContext) -> None:
    ref_code = message.text[7:]

    if ref_code:
        await increment_referral_start(ref_code)
        await state.update_data(ref_code=ref_code)

    video_path = os.path.join(os.getcwd(), 'media', 'sample.mp4')

    await message.answer_video(
        video=FSInputFile(video_path),
        caption=f"<b>🌟 GLOBAL WOMEN FORUM – SIZNING O‘ZGARISH NUQTANGIZ!</b>\n\n"
                f"<b>💫 Faqat bir kun O‘zbekistonning eng top spikerlari siz bilan!</b>\n\n"
                f"<b>🎉 Mehmon spiker —</b>milliarderlar ustozi Mirzakarim Norbekov.\n\n"
                f"📍 Forumda sizni quyidagi mavzular kutmoqda:\n\n"
                f"<b>➖ Ra'no Muminova –</b> Ayollik jozibasini saqlagan holda muammolarni hal qilish siri.\n\n"
                f"<b>➖ Lola Zunnunova –</b>Baxtli oila qoidalari: amaliy maslahatlar.\n\n"
                f"<b>➖ Diyora Keldiyorova –</b>Olimpiya g‘alabasi ortidagi kuch, sabr va motivatsiya.\n\n"
                f"<b>➖ Barno Tursunova –</b>Ayollarga hos biznes: 0 dan 100 milliongacha yo‘l.\n\n"
                f"<b>➖ Oydinoy To‘xtayeva –</b>Zamonaviy ayolning kiyim va imidj orqali muvaffaqiyatga erishishi.\n\n"
                f"<b>➖ Hurriyat Rahmatullayeva –</b> Ongli ota-onalik: bolalar bilan nizolarni hal qilish yo‘llari.\n\n"
                f"<b>🎶 Musiqiy mehmon – O‘zbekiston primadonnasi Yulduz Usmonova!</b>\n\n"
                f"<b>🔥 Sotuv ochilishi munosabati bilan maxsus chegirma!</b>\n\n"
                f"Hoziroq telegram bot orqali menejersiz to‘lovni amalga oshiring va biletlarni <b>deyarli yarim narxida</b> qo‘lga kiriting!\n\n"
                f"<b>📍 20-APREL SANASIDA \"Xalqlar do‘stligi\" saroyida uchrashguncha!</b>",
        reply_markup=get_start_kb(),
        parse_mode="HTML"
    )

@user.message(F.text == "🎫 Chipta sotib olish")
async def choice_rate(message: Message, state: FSMContext) -> None:
    await state.set_state(UserRateStates.phone_number)
    await message.answer(
        text=f"Iltimos, telefor raqamingizni kiriting",
        reply_markup=request_number()
    )

@user.message(UserRateStates.phone_number, F.contact)
async def get_user_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone_number=message.contact.phone_number)
    await message.answer(
        text="Tarifni tanlang👇",
        reply_markup=get_inline_rates()
    )
    data = await state.get_data()
    ref_code = data.get('ref_code')

    if ref_code:
        await increment_referral_number(ref_code)

    await state.set_state(UserRateStates.rate)

@user.callback_query(F.data.startswith("rate_"), UserRateStates.rate)
async def selected_rate(callback: CallbackQuery, state: FSMContext) -> None:
    rate_value = callback.data.split("_")[1]
    await state.update_data(
        name=callback.from_user.first_name,
        rate=rate_value
    )
    data = await state.get_data()
    await callback.message.answer(
        text=f"Ism: {data['name']}\n"
        f"Tarif: <b>{data['rate'].upper()}</b>\n"
        f"Telefon raqami: {data['phone_number']}",
        reply_markup=get_payment_methods()
    )
    await callback.answer()

@user.message(F.text == "💳 Payme")
async def payment_method_payme(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    ref_code = data.get("ref_code")
    ref_username = await get_referral_username(ref_code) if ref_code else "Без реферала"
    data.update({
        "telegram_id": message.from_user.id,
        "username": message.from_user.username
    })
    try:
        result = await create_order(data)

        await message.answer(
                f"🎫 Chipta: <b>{result['order']['ticket_name'].upper()}</b>\n"
                f"💵 Narxi: <b>{result['order']['total_cost']}</b> so'm\n"
                f"📞 Raqam: <b>{result['order']['phone_number']}</b>\n",
            reply_markup=get_pay_link(result['payment_link']))

        await message.bot.send_message(
            chat_id=-1002649801891,
            message_thread_id=5,
            text=f"🟡 ЗАЯВКА\n\n"
                 f"👤 Клиент - <b>{result['order']['customer_name']}</b>\n"
                 f"🎫 Билет - <b>{result['order']['ticket_name'].upper()}</b>\n"
                 f"💵 Сумма платежа - <b>{result['order']['total_cost']} сум</b>\n"
                 f"📞 Номер - {result['order']['phone_number']}\n"
                 f"👥 Реферал: <b>{ref_username}</b>"
        )
        await state.clear()
    except KeyError:
        await message.answer("<b>Bu telegram foydalanuvchisiga to'lov uchun check jo'natilgan.</b>")