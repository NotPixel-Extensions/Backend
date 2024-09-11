from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import User, Pictures

class CreateUserAPIView(APIView):
    async def post(self, request):
        telegram_id = request.data.get('telegram_id')
        if not telegram_id:
            return Response({"error": "telegram_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = await User.objects.aget_or_create(telegram_id=telegram_id)
        if created:
            return Response({"message": "User created", "telegram_id": user.telegram_id}, status=status.HTTP_201_CREATED)
        return Response({"message": "User already exists", "telegram_id": user.telegram_id}, status=status.HTTP_200_OK)


class UpdateLastRequestAPIView(APIView):
    async def post(self, request, telegram_id):
        try:
            user = await User.objects.aget(telegram_id=telegram_id)
            user.last_request = timezone.now()
            await user.asave()
            return Response({"message": "Last request time updated"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class CreatePictureAPIView(APIView):
    async def post(self, request, user_id):
        try:
            user = await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.get('data')
        if not data:
            return Response({"error": "Data field is required"}, status=status.HTTP_400_BAD_REQUEST)

        picture = await Pictures.objects.acreate(user=user, data=data)
        return Response({
            "message": "Picture created",
            "picture_id": picture.id,
            "data": picture.data
        }, status=status.HTTP_201_CREATED)


class ListUserPicturesAPIView(APIView):
    async def get(self, request, telegram_id):
        try:
            user = await User.objects.aget(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


        pictures = await Pictures.objects.filter(user=user).avalues('id', 'data')
        pictures_data = list(pictures)  # Преобразую кверисет в список

        return Response({
            "user": user.telegram_id,
            "pictures": pictures_data
        }, status=status.HTTP_200_OK)
