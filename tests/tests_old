# @pytest.mark.usefixtures("test_client")
# def test_create_user(test_client):
#     """Test the creation of a new user."""
#     response = test_client.post(
#         "/user/",
#         json={"username": "testuser", "email": "testuser@example.com", "password": "password123"}
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["username"] == "testuser"
#
#
# @pytest.mark.usefixtures("test_client")
# def test_get_all_users(test_client):
#     """Test retrieving all users and creating additional users."""
#     response = test_client.get("/user/")
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) == 1
#     assert response.json()[0]["username"] == "testuser"
#     assert response.json()[0]["email"] == "testuser@example.com"
#     assert "password" not in response.json()[0]
#
#     response = test_client.post(
#         "/user/",
#         json={"username": "testuser", "email": "testuser@example.com", "password": "password123"}
#     )
#     assert response.status_code == status.HTTP_400_BAD_REQUEST
#
#     for i in range(1, 4):
#         response = test_client.post(
#             "/user/",
#             json={"username": f"testuser{i}", "email": f"testuser{i}@example.com", "password": "password123"}
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     response = test_client.get("/user/")
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) == 4
#     assert response.json()[1]["username"] == "testuser1"
#     assert response.json()[2]["username"] == "testuser2"
#     assert response.json()[3]["username"] == "testuser3"
#
#
# @pytest.mark.usefixtures("test_client")
# def test_authenticate_user(test_client):
#     """Test user authentication and token retrieval."""
#     response = test_client.post(
#         "/token",
#         data={"username": "testuser", "password": "password123"}
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert "access_token" in response.json()
#     assert "username" in response.json()
#     assert response.json()["username"] == "testuser"
#     return response.json()["access_token"]
#
#
# @pytest.mark.usefixtures("test_client")
# def test_create_post(test_client):
#     """Test creating a new post."""
#     token = test_authenticate_user(test_client)
#     headers = {"Authorization": f"Bearer {token}"}
#     response = test_client.post(
#         "/posts/",
#         json={
#             "title": "Test Post",
#             "content": "This is a test post",
#             "published": True,
#             "creator_id": 1
#         },
#         headers=headers
#     )
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["title"] == "Test Post"
#
#
# @pytest.mark.usefixtures("test_client", "test_db")
# def test_delete_user(test_client, test_db):
#     """Test deleting a user."""
#     user_id = test_db.query(DbUser).filter(DbUser.username == "testuser").first().id
#     response = test_client.delete(f"/user/{user_id}")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["success"] is True
