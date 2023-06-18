from django.shortcuts import render,redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime

def index(request):
    if request.method =="POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
            
    expenses = Expense.objects.all()
    total_exp = expenses.aggregate(total=Sum('amount'))


    last_year = datetime.date.today() - datetime.timedelta(days=365)
    yearly_expenses = Expense.objects.filter(date__gt=last_year)
    yearly_sum = yearly_expenses.aggregate(total=Sum('amount'))

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    monthly_expenses = Expense.objects.filter(date__gt=last_month)
    monthly_sum = monthly_expenses.aggregate(total=Sum('amount'))

    last_week = datetime.date.today() - datetime.timedelta(days=7)
    weekly_expenses = Expense.objects.filter(date__gt=last_week)
    weekly_sum = weekly_expenses.aggregate(total=Sum('amount'))

    daily_sums=Expense.objects.filter().values('date').order_by("date").annotate(sum=Sum('amount'))
    expense_form = ExpenseForm()
    return render(request,'trakapp/index.html',{'expense_form':expense_form,'expenses':expenses,"total_exp": total_exp,"yearly_sum": yearly_sum,"monthly_sum":monthly_sum,"weekly_sum": weekly_sum,"daily_sums":daily_sums})

def edit(request,id):
    expense=Expense.objects.get(id=id)
    
    expense_form = ExpenseForm(instance=expense)
    if request.method =="POST":
        expense=Expense.objects.get(id=id)
        form =ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request,"trakapp/edit.html",{"expense_form": expense_form})


def delete(request,id):
    if request.method == 'POST' and 'delete' in request.POST:
        expense=Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')