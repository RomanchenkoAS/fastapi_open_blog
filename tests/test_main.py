import pytest
from fastapi import status

from db.models import DbBlogPost


@pytest.mark.usefixtures("test_client")
def test_root(test_client):
    """Test root route"""
    response = test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    response = test_client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.usefixtures("test_client", "test_db")
def test_database(test_client, test_db):
    """
    Test basic database operations
    - Make sure the database is up and running
    - Check that migrations are applied correctly
    - Test insertion and retrieval of DbBlogPost objects
    """
    # Create a test blog post associated with the author
    blog_post = DbBlogPost(
        title="Test Blog Post",
        content="This is a test blog post content.",
        author="Test Author",
    )
    test_db.add(blog_post)
    test_db.commit()
    test_db.refresh(blog_post)

    # Assert the blog post was correctly inserted
    assert blog_post.id is not None
    assert blog_post.title == "Test Blog Post"
    assert blog_post.content == "This is a test blog post content."
    assert blog_post.author == "Test Author"

    # Query the database to ensure the objects were inserted correctly
    queried_blog_post = (
        test_db.query(DbBlogPost).filter(DbBlogPost.id == blog_post.id).first()
    )

    assert queried_blog_post is not None
    assert queried_blog_post.id == blog_post.id
    assert queried_blog_post.title == "Test Blog Post"
    assert queried_blog_post.content == "This is a test blog post content."
    assert queried_blog_post.author == "Test Author"
