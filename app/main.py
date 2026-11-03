from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.staticfiles import StaticFiles


from app.routers.processor.router import router as processor_router

from app.features.scoring.service import ScoringService
from app.features.pairing.service import PairingService
from app.features.processing.service import ProcessingService
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler
)
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

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

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(processor_router)

print("MAIN FILE:", __file__)
print("APP TITLE:", app.title)
print("APP ROUTES:")

for route in app.routes:
    print(getattr(route, "path", None))


@app.get("/health1", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


ui_dist = Path(__file__).resolve().parent.parent / "ui" / "dist"
if ui_dist.is_dir():
    app.mount("/", StaticFiles(directory=ui_dist, html=True), name="ui")
