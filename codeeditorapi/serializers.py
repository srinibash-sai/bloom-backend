from rest_framework import serializers
import bcrypt
from .utils import *


class UserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField()
    password = serializers.CharField(max_length=30, write_only=True)
    name = serializers.CharField(max_length=200)

    def save(self):
        data = self.validated_data

        password = data.pop('password', None)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        collection = db['users']

        data['hashed_password'] = hashed_password.decode('utf-8')
        result = collection.insert_one(data)
        return result.inserted_id

    def validate_email(self, value):
        collection = db['users']

        existing_user = collection.find_one({'email': value})
        if existing_user:
            raise serializers.ValidationError("Email already exists.")

        return value


class QuestionSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.CharField(source='_id', read_only=True)
    question = serializers.CharField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['id'] = str(ret['id'])

        return ret
