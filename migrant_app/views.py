from django import forms
from django.contrib import admin, messages
from django.urls import path, include
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponse
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import cv2
import numpy as np
from django.db.models import Q
from django.core.exceptions import ValidationError
import re
from django.contrib import messages
from .models import MigrantWorker
from .forms import UserRegisterForm, MigrantWorkerForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from .forms import ApplicationForm
from .models import Application



# ✅ Real-time Username Check API
def check_username(request):
    username = request.GET.get('username', None)
    if username:
        is_available = not User.objects.filter(username=username).exists()
        return JsonResponse({'available': is_available})
    return JsonResponse({'available': False})


# ✅ User Role Check Functions
def is_admin(user):
    return user.is_authenticated and user.is_superuser

def is_authority(user):
    return user.groups.filter(name='Authority').exists()


# ✅ Home Page
def home(request):
    return render(request, 'home.html', {'logo': 'static/logo.png'})


# ✅ Register User & Generate QR Code
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        worker_form = MigrantWorkerForm(request.POST)

        if user_form.is_valid() and worker_form.is_valid():
            print("✅ Forms are valid!")  # Debugging

            # ✅ Create User & Hash Password
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password1"])  # ✅ Hash password before saving
            user.is_active = False  # Approval required
            user.save()

            # ✅ Create Migrant Worker Entry
            worker = worker_form.save(commit=False)
            worker.user = user
            worker.status = "verifying"  # ✅ Default status before approval
            worker.save()

            print(f"✅ Worker {worker.full_name} registered. Status: {worker.status}")  # Debugging

            return render(request, 'registersuccess.html')

        else:
            print("❌ Form Errors:", user_form.errors.as_json(), worker_form.errors.as_json())  # Debugging

    else:
        user_form = UserRegisterForm()
        worker_form = MigrantWorkerForm()

    return render(request, 'register.html', {'user_form': user_form, 'worker_form': worker_form})


# ✅ Dashboard - Only for Approved Users

@login_required
def dashboard(request):
    # ✅ If user is an admin, redirect to authority dashboard
    if request.user.is_superuser or request.user.groups.filter(name='Authority').exists():
        return redirect('authority_dashboard')  # ✅ Redirect to authority dashboard

    # ✅ Check if the user is a registered migrant worker
    try:
        worker = MigrantWorker.objects.get(user=request.user)
    except MigrantWorker.DoesNotExist:
        messages.error(request, "You are not registered as a migrant worker.")
        return redirect('home')

    # ✅ Only approved workers can access the dashboard
    if worker.status != "approved":
        messages.error(request, "Your account has not been approved yet.")
        return redirect('home')

    # ✅ Render dashboard if approved
    return render(request, 'dashboard.html', {'worker': worker})




# ✅ Admin Dashboard - Approve Workers
def admin_dashboard(request):
    workers = MigrantWorker.objects.filter(status="verifying")  # Fetch workers pending verification
    return render(request, 'admin_dashboard.html', {'workers': workers})


@login_required  # ✅ Ensures the user is logged in
@user_passes_test(is_authority, login_url='/accounts/login/')  # ✅ Ensures the user is an authority
def approve_worker(request, worker_id):
    worker = get_object_or_404(MigrantWorker, id=worker_id)

    if worker.user:
        print(f"Approving Worker: {worker.full_name}")  # Debugging

        worker.status = "approved"
        worker.user.is_active = True  # Activate login
        worker.user.save(update_fields=['is_active'])  # Save only `is_active`
        worker.save(update_fields=['status'])
        
        print(f"Worker Approved: {worker.full_name} | Active Status: {worker.user.is_active}")  # Debugging
        send_status_email(worker)
        messages.success(request, f"{worker.full_name} has been approved and can now log in!")
        return redirect('authority_dashboard')

    else:
        print("Error: No user linked to this worker.")  # Debugging
        messages.error(request, "Error: No user linked to this worker.")

    return redirect('admin_dashboard')

# ✅ Authority Dashboard - View Pending Workers
@login_required
@user_passes_test(is_authority)
def authority_dashboard(request):
    pending_workers = MigrantWorker.objects.filter(status="verifying")  # ✅ Fetch only "Verifying" status workers

    return render(request, 'authority_dashboard.html', {'pending_workers': pending_workers})


# ✅ Reject Worker (Authority)
@login_required
@user_passes_test(is_authority)
def reject_worker(request, worker_id):
    worker = get_object_or_404(MigrantWorker, id=worker_id)

    # ✅ Instead of deleting, update the status to "rejected"
    worker.status = "rejected"
    worker.save()

    messages.success(request, f"{worker.full_name} has been rejected ❌")
    return redirect('authority_dashboard')


# ✅ Verify QR Code Page
def verify_qr_page(request):
    return render(request, 'verify_qr.html', {'logo': 'static/logo.png'})


# ✅ Process QR Code Verification
@login_required
def verify_qr_code(request):
    if request.method == 'POST' and request.FILES.get('qr_image'):
        file = request.FILES['qr_image'].read()
        image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(image)

        print("✅ Extracted QR Code Data:", data)  # Debugging log

        if data:
            # Extract Aadhaar number using regex (assuming it's exactly 12 digits)
            match = re.search(r'\b\d{12}\b', data)
            if match:
                aadhaar_number = match.group(0)  # Extracted Aadhaar number
                print("✅ Extracted Aadhaar Number:", aadhaar_number)  # Debugging log

                # Query the database with extracted Aadhaar number
                worker = MigrantWorker.objects.filter(Q(aadhaar_number=aadhaar_number) & Q(status="approved")).first()

                if worker:
                    print("✅ Worker Found:", worker.full_name)  # Debugging log
                    return JsonResponse({
                        'status': 'success',
                        'full_name': worker.full_name,
                        'aadhaar_number': worker.aadhaar_number,
                        'work_location': worker.work_location
                    })
                else:
                    print("❌ No Matching Worker Found or Not Approved")  # Debugging log
                    return JsonResponse({'status': 'error', 'message': 'Worker not found or not approved'})

            print("❌ Aadhaar Number Not Found in QR Code Data")  # Debugging log
            return JsonResponse({'status': 'error', 'message': 'Invalid QR Code data format'})

        print("❌ Invalid QR Code")  # Debugging log
        return JsonResponse({'status': 'error', 'message': 'Invalid QR Code'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def check_status(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")

        try:
            worker = MigrantWorker.objects.get(phone_number=phone_number)
            status = worker.status  # ✅ Ensure we use the correct field

            # ✅ Fix: Ensure proper status messages
            status_messages = {
                "approved": "✅ Your application has been approved!",
                "rejected": "❌ Your application has been rejected. Please contact support.",
                "validating": "⏳ Your application is currently being validated.",
                "verifying": "🔍 Your application is under review.",
            }
            message = status_messages.get(status, "Unknown status.")

            return JsonResponse({"status": status, "message": message})
        except MigrantWorker.DoesNotExist:
            return JsonResponse({"error": "Phone number not found. Please check and try again."})

    return render(request, "check_status.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')  # ✅ Redirect after successful login
            else:
                return render(request, 'registration/login.html', {'error': 'Your account is inactive'})
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})

    return render(request, 'registration/login.html')

print("✅ migrant_app.views is loaded successfully!")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Send email (Optional)
        send_mail(
            f"New Contact Form Submission from {name}",
            f"Email: {email}\n\nMessage:\n{message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
        )

        return redirect("thank_you")  # Redirect to the thank you page

    return render(request, "contact.html")

def thank_you(request):
    return render(request, "thank_you.html")

def check_email(request):
    email = request.GET.get("email", None)
    if MigrantWorker.objects.filter(email=email).exists():
        return JsonResponse({"available": False})  # ❌ Email Taken
    return JsonResponse({"available": True})  # ✅ Email Available


def send_status_email(worker):
    if worker.status.lower() != "approved":
        print("❌ Email not sent. Worker is not approved.")
        return
    
    subject = f"Application Status Update - {worker.full_name}"
    message = f"""
    Dear {worker.full_name},

    Your application status has been updated to: {worker.status}.
    
    If you have any questions, please contact support.

    Thank you!
    """
    recipient = worker.email

    if not recipient:
        print("❌ No Email Found for Worker")  # Debugging Log
        return

    print(f"📧 Sending Email to {recipient} | Subject: {subject}")  # Debugging Log

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        print("✅ Email sent successfully!")  # Debugging Log
    except Exception as e:
        print(f"❌ Email failed: {e}")  # Debugging Log


def send_status_sms(worker):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message_body = f"Hello {worker.full_name}, your application status is now: {worker.status}."

    print(f"📲 Sending SMS to {worker.phone_number} | Message: {message_body}")  # Debugging Log

    try:
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=worker.phone_number,
        )
        print(f"✅ SMS Sent! SID: {message.sid}")  # Debugging Log
    except Exception as e:
        print(f"❌ SMS Failed: {e}")  # Debugging Log
def apply(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # ✅ Link application to logged-in user
            application.save()
            return redirect("thank_you")  # Redirect after submission

    else:
        form = ApplicationForm()
    return render(request, "apply.html", {"form": form})

