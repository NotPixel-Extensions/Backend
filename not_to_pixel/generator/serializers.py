from rest_framework import serializers
from .models import Pictures

class PicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = ['id', 'user', 'data']  # Список полей для сериализации

    id = serializers.UUIDField(read_only=True)  # Поле для уникального идентификатора
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Связь с пользователем
    data = serializers.JSONField()  # Поле для хранения JSON
