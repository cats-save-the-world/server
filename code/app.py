from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
import uvicorn

from code import auth, game, shop
from code.config import settings, TORTOISE_CONFIG

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(auth.router, prefix='/auth')
app.include_router(game.router, prefix='/games')
app.include_router(shop.router, prefix='/shop')
register_tortoise(app, config=TORTOISE_CONFIG)

if __name__ == '__main__':
    uvicorn.run('code.app:app', host='0.0.0.0', reload=settings.debug)  # pragma: no cover
