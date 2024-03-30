import os
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.routers.data_add import data_add_router
from src.routers.data_edit import data_edit_router
from src.routers.data_get import data_get_router
from src.routers.user import user_router
from src.utils.client import getCockroachClient, getFirebaseClient

app = FastAPI(title="Financial Nexus Backend", version="0.1.1-dev9")

origins = os.environ["CORS_ORIGINS"].split(",")


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()

        try:
            response = await call_next(request)
        except HTTPException as exc:
            response = exc

        end_time = time.time()
        process_time = end_time - start_time
        print(
            f"Request {request.method} {request.url} processed in {process_time:.5f} seconds"
        )

        return response


app.add_middleware(TimingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def startup_event() -> None:
    getCockroachClient()
    getFirebaseClient()


"""@app.middleware("http")
async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as http_exception:
        return http_exception
    except Exception as e:
        return Response(
            content="Internal Server Error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )"""


app.add_event_handler("startup", startup_event)
app.include_router(user_router)
app.include_router(data_add_router)
app.include_router(data_get_router)
app.include_router(data_edit_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=80, reload=True)
