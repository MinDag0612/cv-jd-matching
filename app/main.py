from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import Request


from app.routers.processor.router import router as processor_router

from app.features.scoring.service import ScoringService
from app.features.pairing.service import PairingService
from app.features.processing.service import ProcessingService

@asynccontextmanager
async def lifespan(app: FastAPI):
    scorer = ScoringService()
    pairer = PairingService()

    app.state.processor = ProcessingService(
        scoring=scorer,
        pairing=pairer,
    )

    yield

    app.state.processor = None

app = FastAPI(
    lifespan=lifespan,
    
    title="Document of API for AI Recuitment supporter",
    description="API service",
    version="0.1.0",
)

app.include_router(processor_router)

print("MAIN FILE:", __file__)
print("APP TITLE:", app.title)
print("APP ROUTES:")

for route in app.routes:
    print(getattr(route, "path", None))


@app.get("/health1", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
