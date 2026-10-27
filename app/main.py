from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.features.processor.router import router as processor_router

from app.features.score.similarity_scorer import SimilarityScorer

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.similarity_scorer = SimilarityScorer()
    yield
    app.state.similarity_scorer = None

app = FastAPI(
    lifespan=lifespan,
    
    
    title="Document of API for AI Recuitment supporter",
    description="API service",
    version="0.1.0",
)

app.include_router(processor_router)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
