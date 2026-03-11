from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_router, user_router


# Initialize app
app = FastAPI(
    title="Learn Mathematics Visually.",
    description="An API for visual mathematics learing.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(user_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Visual mathematics learning API."}
