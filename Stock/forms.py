from django import forms
from django.forms import fields
from .models import Stock

class StockCreateForm(forms.ModelForm):
    class Meta:
     model = Stock
     fields = ['item_name', 'quantity']
     
     #Custom form validation    
    def clean_item_name(self):
      item_name = self.cleaned_data.get('item_name')
      if not item_name:
        raise forms.ValidationError('This field is required')
      for instance in Stock.objects.all():
        if instance.item_name == item_name:
          raise forms.ValidationError(item_name + ' already exists')
      return item_name
 
class StockSearchForm(forms.ModelForm):
  class Meta:
    model = Stock
    fields = ['item_name']

class StockIssuedSearchForm(forms.ModelForm):
  export_to_CSV = forms.BooleanField()
  class Meta:
    model = Stock
    fields = ['item_name']
    


class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['item_name', 'quantity']

class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']