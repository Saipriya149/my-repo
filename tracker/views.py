from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import urllib, base64
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from matplotlib.dates import DateFormatter


import calendar
from datetime import datetime
from django.db.models import Sum

from django.conf import settings
import os

import numpy as np
from matplotlib.ticker import MultipleLocator
# tracker/views.py


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'tracker/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def index(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/index.html', {'expenses': expenses})

@login_required
def profile(request):
    return render(request, 'tracker/profile.html')

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('index')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('index')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})

@login_required
@login_required
def expense_chart(request):
    expenses = Expense.objects.filter(user=request.user, date__gte=timezone.now()-timedelta(days=7)).order_by('date')
    dates = [expense.date for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, amounts, marker='o')
    plt.title('Expenses Over Last Week')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    print(uri)  # Add this line to print the URI in the console for debugging

    return render(request, 'tracker/expense_chart.html', {'data': uri})



@login_required
def dashboard(request):
    # Get the current year
    current_year = datetime.now().year

    # Initialize a dictionary to hold monthly expenses
    monthly_expenses = {month: 0 for month in range(1, 13)}

    # Query the database for expenses in the current year
    expenses = Expense.objects.filter(date__year=current_year, user=request.user)

    # Sum expenses for each month
    for expense in expenses:
        month = expense.date.month
        monthly_expenses[month] += expense.amount

    # Convert dictionary to lists for chart.js
    months = [calendar.month_name[month] for month in monthly_expenses.keys()]
    expenses = [monthly_expenses[month] for month in monthly_expenses.keys()]

    return render(request, 'tracker/dashboard.html', {
        'months': months,
        'expenses': expenses,
    })

@login_required
@login_required



def logout_view(request):
    logout(request)
    # Redirect to a success page or another page after logout
    return redirect('home')    