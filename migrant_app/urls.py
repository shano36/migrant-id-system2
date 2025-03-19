from django.urls import path
from .views import home, register, dashboard, admin_dashboard, authority_dashboard, approve_worker, verify_qr_page, verify_qr_code
from .views import contact
from .views import check_username
from . import views
from .views import contact, thank_you
from .views import check_email
from .views import user_login
from .views import verify_worker
from .views import reject_worker

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('authority-dashboard/', authority_dashboard, name='authority_dashboard'),
    path('approve-worker/<int:worker_id>/', approve_worker, name='approve_worker'),
    path('verify-qr/', verify_qr_page, name='verify_qr_page'),
    path('verify-qr-code/', verify_qr_code, name='verify_qr_code'),
    path('check-username/', check_username, name='check_username'),
    path('check-status/', views.check_status, name='check_status'),
    path('', views.home, name='home'),
    path("contact/", contact, name="contact"),
    path("thank-you/", thank_you, name="thank_you"),
    path("check-email/", check_email, name="check_email"),
    path("login/", user_login, name="login"),
    path('verify-worker/<int:worker_id>/', verify_worker, name='verify_worker'),
    path('reject-worker/<int:worker_id>/', reject_worker, name='reject_worker'),
]
