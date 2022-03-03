from datetime import timedelta

from django import forms
from django.utils import timezone, dateformat

from .models import Product


formatted_date = dateformat.format(timezone.now(), 'Y-m-d H:i')

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name_product', 'image_product', 'stock', 'price', 'manufacturer', 'product_type', 'due_date']
        labels = {
            'name_product': 'Name of product',
            'image_product': 'Image product',
            'stock': 'Quantity',
            'price': 'Price',
            'manufacturer': 'Maker',
            'product_type': 'Kind of product',
            'due_date': 'Due date'
        }

        widgets = {
            'name_product': forms.TextInput(
                attrs = {
                    'class': 'form-control rounded',
                    'placeholder': 'Product name'
                }
            ),
            'stock': forms.NumberInput(),
            'price': forms.NumberInput(),
            'manufacturer': forms.Select(),
            'product_type': forms.Select(),
            'due_date': forms.DateTimeInput(
                format = '%Y-%m-%d %H:%M',
                attrs = {
                    # 'type': 'date',
                    'value': formatted_date
                }
            )
        }
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 1 or stock > 100:
            raise forms.ValidationError("Enter a number greater than 0 and less than 100", code='invalid')
        return stock

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 1:
            raise forms.ValidationError('The price must be greater than 0', code='invalid')
        return price

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < (timezone.now() + timedelta(10)):
            self.add_error('due_date', 'Due date must be greater tha 10 dyas after today')
        return due_date