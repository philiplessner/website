def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Phil Lessner" in response.data


def test_blog_page(test_client):
    response = test_client.get('/blog')
    assert response.status_code == 200
    assert b"Blog" in response.data


def test_photos_pages(test_client):
    response = test_client.get('/photos/ecuador')
    assert response.status_code == 200
    assert b"Ecuador" in response.data
    response = test_client.get('/photos/brazil')
    assert response.status_code == 200
    assert b"Brazil" in response.data
    response = test_client.get('/photos/china')
    assert response.status_code == 200
    assert b"China" in response.data
    response = test_client.get('/photos/malaysia')
    assert response.status_code == 200
    assert b"Malaysia" in response.data
    response = test_client.get('/photos/australia')
    assert response.status_code == 200
    assert b"Australia" in response.data
    response = test_client.get('/photos/ghana')
    assert response.status_code == 200
    assert b"Ghana" in response.data
    response = test_client.get('/photos/Uganda')
    assert response.status_code == 200
    assert b"Uganda" in response.data
    response = test_client.get('/photos/france')
    assert response.status_code == 200
    assert b"France" in response.data
    response = test_client.get('/photos/turkey')
    assert response.status_code == 200
    assert b"Turkey" in response.data


def test_aboutme_page(test_client):
    response = test_client.get('/aboutme')
    assert response.status_code == 200
    assert b"Papers" in response.data
    assert b"Patents" in response.data