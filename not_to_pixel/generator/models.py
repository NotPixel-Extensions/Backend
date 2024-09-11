from django.db import models

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)  # Telegram ID, уникальный для каждого пользователя
    last_request = models.DateTimeField(auto_now=True)  # Время последнего взаимодействия с приложением

    def __str__(self):
        return f'User {self.telegram_id}'


class Pictures(models.Model):
    user = models.ForeignKey(User, related_name='pictures', on_delete=models.CASCADE)  # Связь с пользователем
    data = models.JSONField()  # Поле для хранения JSON

    def __str__(self):
        return f'Picture {self.id} for User {self.user.telegram_id}'