from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.features.extractor.router import router as extractor_router
from app.features.parser.router import router as parser_router

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

app.include_router(parser_router)
app.include_router(extractor_router)

@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
