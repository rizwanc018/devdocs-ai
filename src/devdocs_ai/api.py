from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from devdocs_ai.auth.database import initialize_database
from devdocs_ai.auth.routes import router as auth_router
from devdocs_ai.rag_routes import router as rag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="DevDocs AI",
    description="Authentication API for DevDocs AI",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(rag_router)
