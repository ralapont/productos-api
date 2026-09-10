def test_create_product(client):
    payload = {
        "name": "Teclado Mecánico RGB",
        "description": "Switch Red, distribución ISO",
        "price": 89.99,
        "stock": 15
    }

    response = client.post("/products/", json=payload)

    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    
    # Validaciones contra ProductResponse
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]
    assert "id" in data and isinstance(data["id"], int)


def test_get_all_products(client):
    # 1. Insertamos un par de productos primero
    p1 = {"name": "Ratón Gaming", "price": 45.0, "stock": 10}
    p2 = {"name": "Monitor 4K", "price": 320.5, "stock": 5}
    
    client.post("/products/", json=p1)
    client.post("/products/", json=p2)

    # 2. Consultamos el endpoint GET
    response = client.get("/products/")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Ratón Gaming"
    assert data[1]["name"] == "Monitor 4K"