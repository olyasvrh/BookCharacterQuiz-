import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Modules.database.models import init_database
from Modules.Controllers.quiz_controller import router as quiz_router
from Modules.Controllers.auth_controller import router as auth_router
from Modules.Controllers.fav_controller import router as fav_router
from Modules.Controllers.genre_controller import router as genre_router
from Modules.Controllers.social_controller import router as social_router
from Modules.Controllers.ai_controller import router as ai_router

init_database()

app = FastAPI(
    title="Книжкова вікторина",
    description="Тест-вікторина 'Хто ти з книжкових персонажів'",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router)
app.include_router(auth_router)
app.include_router(fav_router)
app.include_router(genre_router)
app.include_router(social_router)
app.include_router(ai_router)


@app.get("/")
async def root():
    return {"message": "Ласкаво просимо до тесту 'Хто ти з книжкових персонажів'!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)