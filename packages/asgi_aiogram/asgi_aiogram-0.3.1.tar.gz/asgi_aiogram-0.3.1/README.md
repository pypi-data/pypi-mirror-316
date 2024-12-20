__base usage__
```python
from aiogram import Dispatcher, Bot
from asgi_aiogram import ASGIAiogram
from asgi_aiogram.strategy import SingleStrategy
from asgi_aiogram.strategy import HttpStrategy
from asgi_aiogram.http_responses import JsonResponse
from asgi_aiogram.http_request import Request

dp = Dispatcher()

@dp.startup()
async def startup(dispatcher: Dispatcher, bot: Bot):
    await bot.close()
    await bot.set_webhook(
        url='https://example.com/bot',
        allowed_updates=dispatcher.resolve_used_update_types()
    )

async def get(request: Request):
    return JsonResponse(body={"status": "ok"})
    
bot = Bot(token="<token>")
app = ASGIAiogram(
        SingleStrategy(path="/bot", bot=bot, dispatcher=dp),
        HttpStrategy(path="/health", method="GET", handler=get),
)
```

```commandline
uvicorn main:app
```
