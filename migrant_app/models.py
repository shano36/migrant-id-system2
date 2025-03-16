from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from .utils import send_status_email, send_status_sms  # Import email & SMS functions


class MigrantWorker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    aadhaar_number = models.CharField(max_length=12, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    work_location = models.CharField(max_length=255)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_workers")

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    STATUS_CHOICES = [
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("validating", "Validating"),
        ("verifying", "Verifying"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="verifying"
    )

    def save(self, *args, **kwargs):
     if self.pk:  # Ensure object already exists
        old_status = MigrantWorker.objects.get(pk=self.pk).status  
        if old_status != self.status and self.updated_by:
            print(f"📩 Sending email and SMS for status change: {self.status}")  # Debugging log
            send_status_email(self)  # ✅ Ensure it's called
            send_status_sms(self)  # ✅ Ensure it's called

    # ✅ Generate QR code if not present
     if not self.qr_code:  
        qr = qrcode.make(f"{self.full_name} - {self.aadhaar_number}")
        qr_io = BytesIO()
        qr.save(qr_io, format='PNG')
        self.qr_code.save(f"{self.aadhaar_number}.png", ContentFile(qr_io.getvalue()), save=False)

     super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.full_name} - {self.status}"


class Application(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending Verification"),
        ("Verified", "Verified"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_applications")

    def __str__(self):
        return f"{self.name} - {self.status}"
