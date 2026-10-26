from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from athletes_base.utils import SEX_CHOICES, RANK_CHOICES, SPORT_CHOICES


class Athlete(models.Model):
    class Meta:
        verbose_name = "Спортсмен"
        verbose_name_plural = "Спортсмены"
        ordering = ["-created_at", "last_name", "first_name"]
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['sport']),
            models.Index(fields=['rank']),
        ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES,verbose_name="Пол")
    sport = models.CharField(max_length=20, choices=SPORT_CHOICES, verbose_name="Вид спорта")
    rank = models.CharField(max_length=5, choices=RANK_CHOICES, default='none', verbose_name="Разряд / Звание")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    team = models.CharField(max_length=150, blank=True, null=True, verbose_name="Клуб / Команда")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    def get_age(self):
        today = date.today()
        age = today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        return age