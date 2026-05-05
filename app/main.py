from fastapi import FastAPI
from app.routes import authRoute,documentRoute,chatRoute,conversationChatRoute
from app.models import userModel
from app.db.session import engine, Base
from app.models import userModel, documentModel   # 👈 ADD THIS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(authRoute.router)
app.include_router(documentRoute.router)
app.include_router(conversationChatRoute.router)
app.include_router(chatRoute.router)