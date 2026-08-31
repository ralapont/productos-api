from sqlmodel import Session, select

from productos_api.models.product import Product
from productos_api.schemas.product import ProductUpdate, ProductCreate


class ProductService:

    @staticmethod
    def create(session: Session, product_create: ProductCreate) -> Product:

        product = Product(**product_create.model_dump())

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    @staticmethod
    def get_all(session: Session):
        statement = select(Product)
        return session.exec(statement).all()

    @staticmethod
    def get_by_id(session: Session, product_id: int) -> Product | None:
        return session.get(Product, product_id)

    @staticmethod
    def delete(session: Session, product: Product) -> None:
        session.delete(product)
        session.commit()

    @staticmethod
    def update(session: Session, product_id: int, product_update: Product,) -> Product | None:

        product = session.get(Product, product_id)

        if not product:
            return None

        update_data = product_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

@staticmethod
def update(session: Session, product_id: int, product_update: ProductUpdate) -> Product | None:

    product = session.get(Product, product_id)

    if not product:
        return None

    update_data = product_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    session.add(product)
    session.commit()
    session.refresh(product)

    return product

            