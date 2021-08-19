import unittest
from flask import request
from werkzeug.wrappers import response

from app import app


class TestApi(unittest.TestCase):
    def test_pt_endpoint_health_returns_200(self):
        with app.test_client() as client:
            response = client.get("/health")
            assert response._status_code == 200

    def test_pt_endpoint_login_get_returns_200(self):
        with app.test_client() as client:
            response = client.get("/login")
            assert response._status_code == 200

    def test_pt_endpoint_login_post_returns_418(self):
        with app.test_client() as client:
            response = client.post("/login")
            assert response._status_code == 418

    def test_pt_endpoint_register_get_returns_200(self):
        with app.test_client() as client:
            response = client.get("/register")
            assert response._status_code == 200

    def test_pt_endpoint_register_post_returns_418(self):
        with app.test_client() as client:
            response = client.post("/register")
            assert response._status_code == 418

    def test_pt_endpoint_dashHome_get_returns_302(self):
        with app.test_client() as client:
            response = client.get("/dash/home")
            assert response._status_code == 302

    def test_pt_endpoint_dashTyper_get_returns_302(self):
        with app.test_client() as client:
            response = client.get("/dash/typer")
            assert response._status_code == 302

    def test_pt_endpoint_dashSettings_get_returns_302(self):
        with app.test_client() as client:
            response = client.get("/dash/settings")
            assert response._status_code == 302

    def test_pt_endpoint_dashSettingsEdit_get_returns_302(self):
        with app.test_client() as client:
            response = client.get("/dash/settings/edit")
            assert response._status_code == 302

    def test_pt_endpoint_dashSignout_get_returns_302(self):
        with app.test_client() as client:
            response = client.get("/dash/signout")
            assert response._status_code == 302
