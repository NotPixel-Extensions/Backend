from django.urls import path
from .views import CreateUserAPIView, UpdateLastRequestAPIView, CreatePictureAPIView, ListUserPicturesAPIView

urlpatterns = [
    path('users/create/', CreateUserAPIView.as_view(), name='create-user'),
    path('users/<int:telegram_id>/update_last_request/', UpdateLastRequestAPIView.as_view(), name='update-last-request'),
    path('users/<int:user_id>/pictures/create/', CreatePictureAPIView.as_view(), name='create-picture'),
    path('users/<int:telegram_id>/pictures/', ListUserPicturesAPIView.as_view(), name='list-user-pictures'),
]