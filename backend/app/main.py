from fastapi import FastAPI
from app.routes import bikes, maintenance, scores
from app.ml.predict import load_models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Predictive Maintenance API")

@app.on_event("startup")
def startup_event():
    load_models()

app.include_router(bikes.router)
app.include_router(maintenance.router)
app.include_router(scores.router)

@app.get("/")
def root():
    return {"message": "Predictive Maintenance API running successfully 🚴‍♂️"}

origins = [
    "http://localhost:4321",
    "http://127.0.0.1:4321",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
