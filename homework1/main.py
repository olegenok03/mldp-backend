from fastapi import FastAPI
from routers.moderation import router as moderation_router

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


app.include_router(moderation_router)
