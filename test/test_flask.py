"""
This is an pytest file for the general page. Here we'll test if you
can submit something on the general page. There is also a validation
on the input data from the user.
"""
import pytest

from src.main import app


@pytest.fixture
def client():
    """
    Here is a client made. With this client we can test
    if you can submit something on the general page.
    """
    app.debug = False
    app.testing = True
    return app.test_client()


def test_root(client):
    """
    Here we use the client to test if you can submit something
    on the general page.
    :return: if every thing is oke, we should get the status code
    200 and the pytest continues. If that's not the case, then the
    pytest will break.
    """
    response = client.get('/')
    assert response.status_code == 200

