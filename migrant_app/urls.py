from django.urls import path
from .views import (
    home, register, dashboard, admin_dashboard, authority_dashboard,
    approve_worker, reject_worker, verify_worker,
    verify_qr_page, verify_qr_code, verify_qr_result, check_status,  # ✅ Added check_status
    contact, thank_you, check_username, check_email, user_login, send_sos_alert, workers_list,track_workers, map_dashboard

)

urlpatterns = [
    path("", home, name="home"),  # ✅ Home Page
    path("register/", register, name="register"),  # ✅ User Registration
    path("dashboard/", dashboard, name="dashboard"),  # ✅ User Dashboard

    # ✅ Admin & Authority Routes
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("authority-dashboard/", authority_dashboard, name="authority_dashboard"),

    # ✅ Worker Management (Approve/Reject/Verify)
    path("approve-worker/<int:worker_id>/", approve_worker, name="approve_worker"),
    path("reject-worker/<int:worker_id>/", reject_worker, name="reject_worker"),
    path("verify-worker/<int:worker_id>/", verify_worker, name="verify_worker"),

    # ✅ QR Code Verification Routes
    path("verify-qr/", verify_qr_page, name="verify_qr_page"),  # ✅ QR Upload Page
    path("verify-qr-code/", verify_qr_code, name="verify_qr_code"),
    path("verify-qr/<str:aadhaar_number>/", verify_qr_result, name="verify_qr_result"),  # ✅ Direct Aadhaar Lookup

    # ✅ Miscellaneous Routes
    path("check-username/", check_username, name="check_username"),
    path("check-status/", check_status, name="check_status"),  # ✅ FIXED!
    path("contact/", contact, name="contact"),
    path("thank-you/", thank_you, name="thank_you"),
    path("check-email/", check_email, name="check_email"),
    path("login/", user_login, name="login"),

    # SOS alert
    path("send_sos_alert/", send_sos_alert, name="send_sos_alert"),
    
    #Tracking workers
    path('workers_list/', workers_list, name='workers_list'),
    path('track_workers/<int:worker_id>/',track_workers,name='track_workers'),

    path('dashboard/', map_dashboard, name='map_dashboard'),  # New map route

]
