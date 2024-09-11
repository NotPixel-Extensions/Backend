from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import User, Pictures

class CreateUserAPIView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(telegram_id=telegram_id)
        if created:
            return Response({"message": "User created", "telegram_id": user.telegram_id}, status=status.HTTP_201_CREATED)
        return Response({"message": "User already exists", "telegram_id": user.telegram_id}, status=status.HTTP_200_OK)


class UpdateLastRequestAPIView(APIView):
    def post(self, request, telegram_id):
        try:
            user = User.objects.get(telegram_id=telegram_id)
            user.last_request = timezone.now()  #Обновляю время последнего запроса
            user.save()
            return Response({"message": "Last request time updated"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class CreatePictureAPIView(APIView):
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.get('data')  #Получаею жсон данные
        if not data:
            return Response({"error": "Data field is required"}, status=status.HTTP_400_BAD_REQUEST)

        picture = Pictures.objects.create(user=user, data=data)
        return Response({
            "message": "Picture created",
            "picture_id": picture.id,
            "data": picture.data
        }, status=status.HTTP_201_CREATED)
    

class ListUserPicturesAPIView(APIView):
    def get(self, request, telegram_id):
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Получаем все картинки пользователя
        pictures = Pictures.objects.filter(user=user)
        pictures_data = [
            {
                "picture_id": picture.id,
                "data": picture.data,
            } for picture in pictures
        ]

        return Response({
            "user": user.telegram_id,
            "pictures": pictures_data
        }, status=status.HTTP_200_OK)