from django.db import models
from manager.models import Car, StagePrice

# Create your models here.

class Receipts(models.Model):
    receipt_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='receipts')
    customer_name = models.CharField(max_length=100)
    customer_contact = models.CharField(max_length=100)
    stage_price = models.ForeignKey(StagePrice, on_delete=models.CASCADE)
    data_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Receipt {self.receipt_id} - {self.customer_name}'