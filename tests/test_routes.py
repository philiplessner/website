def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Phil Lessner" in response.data



def test_blog_page(test_client):
    response = test_client.get('/blog')
    assert response.status_code == 200
    assert b"Blog" in response.data