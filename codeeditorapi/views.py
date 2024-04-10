from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, QuestionSerializer
import jwt, datetime
from .utils import *
import bcrypt
from bson import ObjectId
import subprocess


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = db['users'].find_one({"email": email})

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': f"{user['_id']}",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        response = Response()

        response.set_cookie(key='token', value=token, httponly=True)
        response.data = {
            'token': token
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': 'success'
        }
        return response


class UserView(APIView):
    def get(self, request):
        user_id = request.user_id

        user = db['users'].find_one({"_id": ObjectId(user_id)})

        serializer = UserSerializer(user)
        return Response(serializer.data)


class PythonView(APIView):
    def post(self, request):
        code = request.data['code']

        process = subprocess.Popen(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        if error:
            response = Response({"success": False, "message": error})
            return response
        else:
            response = Response({"success": True, "message": "Success", "output": output})
            return response


class PythonQuestionView(APIView):
    def get(self, request):
        questions = db['questions'].find()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class PythonSubmitView(APIView):
    def post(self, request):
        code = request.data['code']
        question_id = request.data['questionId']
        try:
            db['questions'].update_one(
                {"_id": ObjectId(question_id)},
                {"$set": {"userCode": code}}
            )
            process = subprocess.Popen(['python', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
            output, error = process.communicate()
            if error:
                response = Response({"success": False, "message": error})
                return response
            else:
                response = Response({"success": True, "message": "Success", "output": output})
                return response
        except Exception as e:
            response = Response({"success": False, "message": str(e)})
            return response
