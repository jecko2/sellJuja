
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from account.utils.serializers import BaseUserSerializer
from account.models import BaseUserModel
import datetime
import jwt


class Register(APIView):
    @staticmethod
    def post(request):
        serializer = BaseUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    @staticmethod
    def post(request):

        email = request.data['email']
        password = request.data['password']
        user = BaseUserModel.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed({"error": "user not found!"})
        if not user.check_password(password):
            raise AuthenticationFailed({"error": "incorrect credentials"})

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret", algorithm='HS256').encode().decode('utf-8')

        response = Response()

        response.set_cookie(key="jwt_cookie", value=token, httponly=True)
        response.data = {
            "jwt_token": token
        }

        return response


class UserView(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get("jwt_cookie")
        if not token:
            raise AuthenticationFailed({"authorizationError": "Unauthorized"})
        try:
            payload = jwt.decode(token, "secret", algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"authorizationError": "Unauthorized"})

        user = BaseUserModel.objects.filter(id=payload['id']).first()
        serializer = BaseUserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    @staticmethod
    def post(self):

        response = Response()
        response.delete_cookie("jwt_cookie")
        response.data = {
            "message": "Logged out successfully"
        }

        return response
