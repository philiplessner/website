from unittest.mock import patch

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


def test_missing_blogpost_returns_not_found(test_client):
    response = test_client.get('/blog/2147483647')
    assert response.status_code == 404


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
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Incorrect Email or Password' in response.data


def analytics_graph_data():
    return {
        'countryCodes': ['US'],
        'endpoints': ['/'],
        'percentages': [100.0],
        'dates': ['2026-08-01'],
        'humans': [1],
        'robots': [1],
        'title': 'Analytics test',
    }


def test_analytics_accepts_dates_within_database_range(test_client):
    graph_data = analytics_graph_data()
    with (
        patch('app.admin.current_user') as current_user,
        patch('app.admin.log_date_bounds', return_value=('2026-07-12', '2026-09-12')),
        patch('app.admin.countryCodes_humans', return_value=graph_data) as country_chart,
        patch('app.admin.countryCodes_robots', return_value=graph_data),
        patch('app.admin.endpoints_humans', return_value=graph_data),
        patch('app.admin.endpoints_robots', return_value=graph_data),
        patch('app.admin.visits', return_value=graph_data),
    ):
        current_user.is_authenticated = True
        response = test_client.post('/analytics', data={
            'start_date': '2026-08-01',
            'end_date': '2026-08-31',
        })

    assert response.status_code == 200
    assert b'id="visitsChart"' in response.data
    country_chart.assert_called_once_with(
        '2026-08-01 00:00:00',
        '2026-08-31 23:59:59',
    )


def test_analytics_rejects_dates_outside_database_range(test_client):
    graph_data = analytics_graph_data()
    with (
        patch('app.admin.current_user') as current_user,
        patch('app.admin.log_date_bounds', return_value=('2026-07-12', '2026-09-12')),
        patch('app.admin.countryCodes_humans', return_value=graph_data),
        patch('app.admin.countryCodes_robots', return_value=graph_data),
        patch('app.admin.endpoints_humans', return_value=graph_data),
        patch('app.admin.endpoints_robots', return_value=graph_data),
        patch('app.admin.visits', return_value=graph_data),
    ):
        current_user.is_authenticated = True
        response = test_client.post('/analytics', data={
            'start_date': '2026-07-01',
            'end_date': '2026-08-31',
        })

    assert response.status_code == 200
    assert b'Dates must be between 2026-07-12 and 2026-09-12.' in response.data
