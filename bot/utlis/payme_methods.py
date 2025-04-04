import aiohttp

TICKET_PRICES = {
    "standart": 1000,
    "comfort": 300_000,
    "business": 480_000,
    "vip": 720_000,
    "platinum": 2_800_000
}

async def create_order(data: dict) -> dict | None:
    ticket_name = data.get("rate", "").lower()
    amount = TICKET_PRICES.get(ticket_name)

    if amount is None:
        return None

    payload = {
        "customer_name": data.get("name"),
        "phone_number": data.get("phone_number"),
        "telegram_id": data.get("telegram_id"),
        "username": data.get("username"),
        "ticket_name": ticket_name,
        "total_cost": amount,
        "payment_method": "payme"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                url="http://localhost:8000/order/create/",
                json=payload
        ) as response:
            result = await response.json()

            return result