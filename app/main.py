import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from core.config import settings
from core.client import check_client_authorized
from api.router import api_router

# Initial Base APP Instance
app = FastAPI(title=settings.PROJECT_NAME)
# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def verify_user_agent(request: Request, call_next):
    url_string = str(request.url)
    index = url_string.find('/private')
    if index > 0:
        user_auth = await check_client_authorized()
        if user_auth:
            response = await call_next(request)
            return response
        else:
            return JSONResponse(content={
                "message": "unauthorized account request"
            }, status_code=401)

    response = await call_next(request)
    return response


app.include_router(api_router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=True)
