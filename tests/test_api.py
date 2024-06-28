import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.models import DbBlogPost


@pytest.mark.usefixtures("test_client", "test_db")
class TestBlogPostEndpoints:

    @pytest.fixture(autouse=True)
    def setup(self, test_db: Session):
        # Create a test author

        raise NotImplementedError("Fix author")
        self.author = DbAuthor(name="Test Author")
        test_db.add(self.author)
        test_db.commit()
        test_db.refresh(self.author)
        self.test_db = test_db

    def test_create_blog_post(self, test_client: TestClient):
        response = test_client.post(
            "/blogpost",
            json={
                "title": "New Blog Post",
                "content": "Content of the new blog post",
                "author_name": self.author.name,
            },
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "New Blog Post"
        assert data["content"] == "Content of the new blog post"
        assert data["author"]["name"] == self.author.name

    def test_get_all_blog_posts(self, test_client: TestClient):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post", content="Some content", author_id=self.author.id
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        response = test_client.get("/blogpost")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["title"] == "Blog Post"
        assert data[0]["content"] == "Some content"
        assert data[0]["author_id"] == self.author.id

    def test_get_single_blog_post(self, test_client: TestClient):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Single Blog Post", content="Some content", author_id=self.author.id
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        response = test_client.get(f"/blogpost/{blog_post.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Single Blog Post"
        assert data["content"] == "Some content"
        assert data["author_id"] == self.author.id

    def test_delete_blog_post(self, test_client: TestClient):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post to Delete", content="Some content", author_id=self.author.id
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        response = test_client.delete(f"/blogpost/{blog_post.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Blog Post to Delete"

        # Verify that the blog post has been deleted
        deleted_blog_post = (
            self.test_db.query(DbBlogPost).filter(DbBlogPost.id == blog_post.id).first()
        )
        assert deleted_blog_post is None

    def test_update_blog_post(self, test_client: TestClient):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post to Update", content="Some content", author_id=self.author.id
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        response = test_client.patch(
            f"/blogpost/{blog_post.id}",
            json={"title": "Updated Blog Post", "content": "Updated content"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Blog Post"
        assert data["content"] == "Updated content"

        # Verify that the blog post has been updated
        updated_blog_post = (
            self.test_db.query(DbBlogPost).filter(DbBlogPost.id == blog_post.id).first()
        )
        assert updated_blog_post.title == "Updated Blog Post"
        assert updated_blog_post.content == "Updated content"

    def test_upload_image_to_blog_post(self, test_client: TestClient):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post with Image", content="Some content", author_id=self.author.id
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        # Create a mock image file
        image_data = b"fake_image_data"
        files = {"file": ("test_image.png", image_data, "image/png")}

        response = test_client.post(f"/blogpost/{blog_post.id}/upload", files=files)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == blog_post.id

        # Verify that the image has been uploaded
        blog_post_with_image = (
            self.test_db.query(DbBlogPost).filter(DbBlogPost.id == blog_post.id).first()
        )
        assert blog_post_with_image.image == image_data
