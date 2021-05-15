from django.contrib import admin
from .forms import StockCreateForm

from .models import Stock

# Register the Stock Model

class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['item_name', 'quantity']
   form = StockCreateForm
   list_filter = ['item_name']
   search_fields = ['item_name']



admin.site.register(Stock, StockCreateAdmin)
