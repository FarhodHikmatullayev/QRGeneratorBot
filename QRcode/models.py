import datetime
from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ('user', 'Oddiy foydalanuvchi'),
        ('cashier', "Kassir"),
        ('admin', 'Admin')
    )
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='F.I.Sh')
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name='Username')
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user', null=True, blank=True,
                            verbose_name='Foydalanuvchi roli')
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True, verbose_name="Telegram ID")
    joined_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Qo'shilgan vaqti")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'
        db_table = 'users'

    def __str__(self):
        return self.full_name


class QrCode(models.Model):
    user_name = models.CharField(max_length=221, null=True, blank=True, verbose_name="QR kod egasi ismi")
    information = models.CharField(unique=True, max_length=30, null=True, blank=True, verbose_name="Qr information")
    is_active = models.BooleanField(default=True, verbose_name="Faollik holati")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Yaratilgan vaqti")

    class Meta:
        verbose_name = 'QRCode'
        verbose_name_plural = 'QR kodlar'
        db_table = 'qrcode'
        ordering = ['-created_at']

    def __str__(self):
        if self.user_name:
            return self.user_name
        else:
            return f'{self.created_at}'
