import httpx
from decimal import Decimal
from app.utils.redis_client import redis_client

EXCHANGE_API_URL="https://open.er-api.com/v6/latest/"

async def get_exchange_rate(from_currency:str,to_currency:str)->Decimal:
    if from_currency==to_currency:
        return Decimal("1.0")
    redis_key=f"rate:{from_currency}_{to_currency}"

    cached_rate=await redis_client.get(redis_key)
    if cached_rate:
        return Decimal(cached_rate)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{EXCHANGE_API_URL}{from_currency}")
        response.raise_for_status()
        data = response.json()

    if data.get("result") != "success":
        raise ValueError("Failed to fetch exchange rates")

    rate = data["rates"].get(to_currency)
    if not rate:
        raise ValueError(f"Cannot convert {from_currency} to {to_currency}")

    decimal_rate = Decimal(str(rate))
    
    await redis_client.set(redis_key, str(decimal_rate), ex=86400)
    
    return decimal_rate

