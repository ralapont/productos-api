from fastapi import FastAPI
from productos_api.api.v1.products import router as products_router

app = FastAPI(
    title="Productos API",
    version="1.0.0"
)

app.include_router(products_router)

@app.get("/")
def health():
    return {"status": "ok"}