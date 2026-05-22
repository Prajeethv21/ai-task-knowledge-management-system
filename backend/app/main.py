from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routers import auth_router, tasks_router, documents_router, search_router, analytics_router, users_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(tasks_router, prefix=settings.api_prefix)
app.include_router(documents_router, prefix=settings.api_prefix)
app.include_router(search_router, prefix=settings.api_prefix)
app.include_router(analytics_router, prefix=settings.api_prefix)
app.include_router(users_router, prefix=settings.api_prefix)


@app.get("/")
def health_check():
    return {"status": "ok"}
