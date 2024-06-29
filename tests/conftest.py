import pytest
from app import create_app, db
from app.models import User, Crime, Prison, Prisoner

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def setup_database(init_database):
    user = User(username='testuser')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    crime = Crime(crime_name='Theft')
    db.session.add(crime)
    db.session.commit()

    prison = Prison(prison_name='Alcatraz')
    db.session.add(prison)
    db.session.commit()

    prisoner = Prisoner(
        name='John Doe',
        age=30,
        gender='Male',
        crime_id=crime.crime_id,
        sentence_years=5,
        prison_id=prison.prison_id
    )
    db.session.add(prisoner)
    db.session.commit()

    yield user, prisoner
