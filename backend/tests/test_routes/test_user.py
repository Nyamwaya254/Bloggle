def test_create_user(client):
    data = {"email":"billy@example.com","password":"Genius"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "billy@example.com"