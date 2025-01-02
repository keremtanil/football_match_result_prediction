from django import forms
from datetime import date

class DateField(forms.Form):
    match_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'max': date.today().strftime('%Y-%m-%d'),
                'placeholder': 'Tarih Seçiniz'
            }
        ),
        initial=date.today,
    )


