from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from productos_api.core.database import get_session
from productos_api.models.product import Product
from productos_api.schemas.product import ProductUpdate, ProductCreate
from productos_api.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=Product)
def create_product(product_create: ProductCreate, session: Session = Depends(get_session)):

    return ProductService.create(session=session, product_create=product_create)

@router.get("/", response_model=list[Product])
def list_products(session: Session = Depends(get_session)):
    return ProductService.get_all(session)

@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    product = ProductService.get_by_id(
        session=session,
        product_id=product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = ProductService.get_by_id(
        session=session,
        product_id=product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    ProductService.delete(
        session=session,
        product=product
    )

    return {
        "message": "Producto eliminado"
    }

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, payload: Product, session: Session = Depends(get_session)):
    product = ProductService.get_by_id(
        session=session,
        product_id=product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    product.name = payload.name
    product.description = payload.description
    product.price = payload.price
    product.stock = payload.stock

    return ProductService.update(session=session, product_id=product_id, product_update=product)

@router.patch("/{product_id}")
def update_product(
    product_id: int,
    payload: ProductUpdate,
    session: Session = Depends(get_session),
):
    product = ProductService.update(
        session=session,
        product_id=product_id,
        product_update=payload,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product