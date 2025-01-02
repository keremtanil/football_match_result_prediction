from django import forms

class DateField(forms.Form):
    match_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Tarih Seçiniz'
            }
        )
    )


