from django.db import models


class Profile(models.Model):
    foreign_id = models.IntegerField(
        verbose_name='Id пользователя'
    )
    id_channel = models.TextField(
        verbose_name='Id канала'
    )
    name = models.TextField(
        verbose_name='Имя'
    )
    tg_tag = models.TextField(
        verbose_name='Тег телеграм'
    )
    birthday = models.DateField(
        verbose_name='День рождения'
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'