from werkzeug.security import generate_password_hash

from app import db
from app.models import User


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


def test_login_with_correct_credentials(test_client):
    with test_client.application.app_context():
        user = User(email='login-success@example.com', password_hash=generate_password_hash('secret123'), name='Test User')
        db.session.add(user)
        db.session.commit()

    response = test_client.post('/login', data={
        'email': 'login-success@example.com',
        'password': 'secret123',
        'remember_me': False,
    }, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/profile')

    with test_client.application.app_context():
        created_user = db.session.scalars(db.select(User).where(User.email == 'login-success@example.com')).first()
        if created_user is not None:
            db.session.delete(created_user)
            db.session.commit()


def test_login_with_incorrect_credentials(test_client):
    response = test_client.post('/login', data={
        'email': 'missing@example.com',
        'password': 'wrong-password',
        'remember_me': False,
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Incorrect Email or Password' in response.data