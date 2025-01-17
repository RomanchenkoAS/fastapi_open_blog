import io

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.models import DbBlogPost


@pytest.mark.usefixtures("test_client", "test_db")
class TestBlogPostEndpoints:

    @pytest.fixture(autouse=True)
    def setup(self, test_db: Session, test_client: TestClient):
        # Create a test author
        self.author = "Test Author"
        self.test_db = test_db
        self.test_client = test_client

    def test_create_blog_post(self):
        image_content = b"this is a test image"
        files = {"image": ("test_image.png", io.BytesIO(image_content), "image/png")}
        response = self.test_client.post(
            "/blogpost",
            data={
                "title": "New Blog Post",
                "content": "Content of the new blog post",
                "author": self.author,
            },
            files=files,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "New Blog Post"
        assert data["content"] == "Content of the new blog post"
        assert data["author"] == self.author

    def test_get_all_blog_posts(self):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post", content="Some content", author=self.author
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        response = self.test_client.get("/blogpost")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["title"] == "Blog Post"
        assert data[0]["content"] == "Some content"
        assert data[0]["author"] == self.author

    def test_get_single_blog_post(self):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Single Blog Post", content="Some content", author=self.author
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        response = self.test_client.get(f"/blogpost/{blog_post.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Single Blog Post"
        assert data["content"] == "Some content"
        assert data["author"] == self.author

    def test_delete_blog_post(self):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post to Delete", content="Some content", author=self.author
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        response = self.test_client.delete(f"/blogpost/{blog_post.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Blog Post to Delete"

        # Verify that the blog post has been deleted
        deleted_blog_post = (
            self.test_db.query(DbBlogPost).filter(DbBlogPost.id == blog_post.id).first()
        )
        assert deleted_blog_post is None

    def test_update_blog_post(self):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post to Update", content="Some content", author=self.author
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        image_content = b"this is a test image"
        files = {"image": ("test_image.png", io.BytesIO(image_content), "image/png")}
        response = self.test_client.patch(
            f"/blogpost/{blog_post.id}",
            data={
                "title": "Updated Blog Post",
                "content": "Updated content",
                "author": self.author,
            },
            files=files,
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

    def test_update_blog_post_incomplete_request(self):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post to Update", content="Some content", author=self.author
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        # Do not change author & body, only title
        response = self.test_client.patch(
            f"/blogpost/{blog_post.id}",
            data={
                "title": "Updated Blog Post",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Blog Post"
        assert data["content"] == "Some content"
        assert data["author"] == self.author

        # Verify that the blog post has been updated
        updated_blog_post = (
            self.test_db.query(DbBlogPost).filter(DbBlogPost.id == blog_post.id).first()
        )
        assert updated_blog_post.title == "Updated Blog Post"
        assert updated_blog_post.content == "Some content"

    def test_upload_image_to_blog_post(self):
        # Create a test blog post
        blog_post = DbBlogPost(
            title="Blog Post with Image", content="Some content", author=self.author
        )
        self.test_db.add(blog_post)
        self.test_db.commit()
        self.test_db.refresh(blog_post)

        image_content = b"this is a test image"
        files = {"image": ("test_image.png", io.BytesIO(image_content), "image/png")}

        response = self.test_client.post(f"/blogpost/{blog_post.id}/upload", files=files)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == blog_post.id

        # Verify that the image has been uploaded
        blog_post_with_image = (
            self.test_db.query(DbBlogPost).filter(DbBlogPost.id == blog_post.id).first()
        )
        assert blog_post_with_image.image == image_content
