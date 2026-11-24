from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from materials.models import Course, Lesson


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="электронная почта",
        help_text="Укажите электронную почту",
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=30, verbose_name="Город", help_text="Укажите ваш город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.email


class Payments(models.Model):
    STATUS_CHOICES = [
        ("cash", "наличные"),
        ("remittance", "денежный перевод"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_of_payment = models.DateTimeField(auto_now=False, verbose_name="Дата оплаты")
    payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="cash",
        verbose_name="Способ оплаты: наличные или перевод на счет",
    )
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.paid_course if self.paid_course else self.paid_lesson} - {self.payment_amount}"

    class Meta:
        verbose_name = "Платежи"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_amount"]
