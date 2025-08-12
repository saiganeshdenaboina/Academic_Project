from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'image', 'current_stock']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
            'category': forms.Select(),
            'image': forms.ClearableFileInput(),
            'current_stock': forms.NumberInput(attrs={'placeholder': 'Enter stock quantity', 'min': 0}),
        }
