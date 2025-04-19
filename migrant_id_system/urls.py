from django.contrib import admin
from django.urls import path, include
from migrant_app import views  # ✅ Import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from migrant_app.views import user_login

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.home, name='home'),  
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('authority-dashboard/', views.authority_dashboard, name='authority_dashboard'),
    path('approve-worker/<int:worker_id>/', views.approve_worker, name='approve_worker'),
    path('verify-qr/', views.verify_qr_page, name='verify_qr_page'),
    path('verify-qr-code/', views.verify_qr_code, name='verify_qr_code'),
    path('authority-dashboard/', views.authority_dashboard, name='authority_dashboard'),
    path('reject-worker/<int:worker_id>/', views.reject_worker, name='reject_worker'),
    # ✅ Authentication URLs (Django Default Uses `accounts/`)
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # ✅ Add this for logout
    path('', include('migrant_app.urls')),
    path('approve-worker/<int:worker_id>/', views.approve_worker, name='approve-worker'),
    path("login/", user_login, name="login"),
    path("map/", map, name="map"),
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
