from django.contrib.auth.base_user import AbstractBaseUser
from django.core.management.base import BaseCommand

from users.models import Payments, User


class Command(BaseCommand):
    help = "Add payments to the database"

    def handle(self, *args, **options):
        user = User.objects.get_or_create(email="test@sky.pro", city="Москва")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        user.set_password("1234")
        user.save()

        payments = [
            {
                "user": user,
                "date_of_payment": "2026-11-11",
                "payment_amount": "10000",
                "payment_method": "cash",
            },
            {
                "user": user,
                "date_of_payment": "2026-11-10",
                "payment_amount": "5000",
                "payment_method": "remittance",
            },
        ]

        for payment_data in payments:
            payment, created = Payments.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added payment: {payment.user}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Payment already exits: {payment.user}")
                )
