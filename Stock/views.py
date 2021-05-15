from functools import wraps
from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv, xlwt
from .models import *
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, StockIssuedSearchForm
from django.contrib import messages
import datetime

# Views.

def home(request):
    title = 'WELCOME TO THE STOCK MANAGEMENT SYSTEM'
    form = "Hello i am form"
    context = {
        "title": title,
    }
    return render(request, "home.html",context)


def list_items(request):
    title = 'STOCK LIST'
    #Filter by Search
    form = StockSearchForm(request.POST or None)
    
    queryset = Stock.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
        "form": form
    }
    if request.method ==  'POST':
        queryset = Stock.objects.filter(item_name__icontains=form['item_name'].value())
        if form['item_name'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.item_name, stock.quantity])
            return response
        context = {
            "form": form,
            "title": title,
            "queryset": queryset,
        }
    return render(request, "list_items.html",context)

def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "ADD STOCK",
    }
    return render(request, "add_items.html", context)

def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/list_items')

    context = {
        'form':form
    }
    return render(request, 'add_items.html', context)

def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/list_items')
    return render(request, 'delete_items.html')

def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)

def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()
        return redirect('/list_items')
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)

def stock_issued(request):
    title = 'ISSUED STORK'
    queryset = Stock_Issued.objects.all()
    form = StockIssuedSearchForm(request.POST or None)
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }    
    if request.method == 'POST':
        item_name = form['item_name'].value()
        queryset = Stock_Issued.objects.filter(
                                item_name__icontains=form['item_name'].value()
                                )
        if (item_name != ''):
            queryset = queryset.filter(item_name_id_id=item_name)
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Issued Stock.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [ 
                'ITEM NAME',
                'QUANTITY', 
                'ISSUE QUANTITY',       
                'ISSUE TO', 
                'DATE'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                [
                stock.item_name, 
                stock.quantity, 
                stock.issue_quantity,  
                stock.issue_to, 
                stock.timestamp])
            return response
        context = {
        "form": form,
        "title": title,
        "queryset": queryset,
    }
    return render(request, "stock_issued.html",context)