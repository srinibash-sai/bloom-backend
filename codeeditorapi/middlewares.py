import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from bson import ObjectId
from pymongo import MongoClient
from django.urls import resolve


JWT_SECRET='ABCDEFCFHgmvmjvmvmv'

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_endpoints = ['/api/login', '/api/register']
        current_url = request.path_info

        if current_url in excluded_endpoints:
            return self.get_response(request)

        token = request.COOKIES.get('token')
        print(token)
        print("bjdbjbjkbekjbwk")

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        request.user_id = ObjectId(payload['id'])

        response = self.get_response(request)
        return response