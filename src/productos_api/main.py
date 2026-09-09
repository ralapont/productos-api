from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from productos_api.api.v1.products import router as products_router

app = FastAPI(
    title="Productos API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React/Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)

@app.get("/")
def health():
    return {"status": "ok"}