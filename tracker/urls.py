from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_expense, name='add_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('chart/', views.expense_chart, name='expense_chart'),
    path('chart/', views.chart, name='chart'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]

