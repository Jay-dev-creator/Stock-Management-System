from django.db import models

# Models.

class Stock(models.Model):
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=False, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	export_to_CSV = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.item_name + '(' + str(self.quantity) + ')'



class Stock_Issued(models.Model):
	
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)