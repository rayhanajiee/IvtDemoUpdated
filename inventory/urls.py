from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Index, Dashboard, AddItem, EditItem, DeleteItem, SignUpView, ExportData
from . import views
from .restapi import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('export-data/', views.ExportData, name='export-data'),  # Correct usage
    path('save-code-description/', views.save_code_description, name='save_code_description'),

    # mobile urls api
    path('api/register/', api_register, name='api_register'),
    path('api/login/', api_login, name='api_login'),
    path('api/check_inventory/', api_check_inventory, name='api_check_inventory'),
    path('api/add_inventory/', api_add_inventory, name='api_add_inventory'),
    path('api/categories/', category_list, name='category_list'),
    path('api/moving/', api_moving, name='moving'),
    path('api/service/', api_service, name='service'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
