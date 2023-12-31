from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.answer import answer_router
from domain.question import question_router
from domain.user import user_router
from domain.place import place_router
from domain.device import device_router

app = FastAPI()

origins = [
    "*",
        #"http://localhost",
        #"http://localhost:80",
        #"http://127.0.0.1",
        #"http://127.0.0.1:80",
        "http://10.0.1.88",
        "http://10.0.1.88:80"
     #"http://localhost:5173"#"http://127.0.0.1:5173",    # 또는 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.include_router(place_router.router)
app.include_router(device_router.router)
#app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))
# app.mount("/", StaticFiles(directory="frontend_flutter/build/web/"))

# @app.get("/")
# def index():
#     #return FileResponse("frontend/dist/index.html")
#     return FileResponse("frontend_flutter/build/web/index.html")