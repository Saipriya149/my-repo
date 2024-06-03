# ExpenseTracker/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from tracker import views as tracker_views  # Ensure this import is correct


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', tracker_views.index, name='index'),
    path('add/', tracker_views.add_expense, name='add_expense'),
    path('expense_chart/', tracker_views.expense_chart, name='expense_chart'),
    #path('chart/', tracker_views.chart, name='chart'),
    path('profile/', tracker_views.profile, name='profile'),
     path('delete/<int:expense_id>/', tracker_views.delete_expense, name='delete_expense'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', tracker_views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
