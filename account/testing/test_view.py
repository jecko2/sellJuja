from rest_framework.test import APITestCase
import datetime
import jwt
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from account.models import BaseUserModel
from account.utils.serializers import BaseUserSerializer

class TestAuthenticationViews(APITestCase):
    register_url = "http://127.0.0.1:8000/account/register/"
    login_url = "http://127.0.0.1:8000/account/login/"
    logout_url = "http://127.0.0.1:8000/account/logout/"

    def test_register(self):
        payload = {
            "email": "test@gmail.com",
            "password": "test123"
        }

        response = self.client.post(self.register_url, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_login(self):
        payload = {
            "email": "test@gmail.com",
            "password": "test123",
        }
        self.client.post(self.register_url, data=payload)

        response = self.client.post(self.login_url, data=payload)

        result = response.json()

        if not result['jwt_token']:
            raise AuthenticationFailed({"authorization": "No user"})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        payload = {
            "email": "test@gmail.com",
            "password": "test123",
        }
        self.client.post(self.register_url, data=payload)
        self.client.post(self.login_url, data=payload)

        response = self.client.post(self.logout_url, data=payload)

        self.assertEqual(response.status_code, 200)


class TestGenericView(APITestCase):
    register_url = "http://127.0.0.1:8000/account/register/"
    login_url = "http://127.0.0.1:8000/account/login/"
    user_url = "http://127.0.0.1:8000/account/user/"

    def test_user_view(self):
        payload_user = {
            "email": "test@gmail.com",
            "password": "test123",
        }
        self.client.post(self.register_url, data=payload_user)
        self.client.post(self.login_url, data=payload_user)

        email = payload_user['email']
        password = payload_user['password']
        user = BaseUserModel.objects.filter(email=email).first()

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret", algorithm='HS256').encode().decode('utf-8')

        if not token:
            raise AuthenticationFailed("Failed authentication")
        try:
            payload = jwt.decode(token, "secret", algorithms=['HS256'])
            user = BaseUserModel.objects.filter(id=payload['id']).first()
            serializer = BaseUserSerializer(user)
    
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        
        self.assertEqual(serializer.data['email'], 'test@gmail.com')
