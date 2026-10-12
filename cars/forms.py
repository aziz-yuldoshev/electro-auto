from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'comment']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism va familiyangiz'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998 90 123 45 67'
            }),

            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Qo‘shimcha izoh...',
                'rows': 4
            }),
        }

