from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
import uvicorn

from code import auth, handlers
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
app.add_api_route('/games', handlers.game_create_handler, methods=['post'])
app.add_api_websocket_route('/games/{game_id}/events', handlers.GameEventsHandler())
register_tortoise(app, config=TORTOISE_CONFIG)

if __name__ == '__main__':
    uvicorn.run('code.app:app', host='0.0.0.0', reload=settings.debug)
