from django import forms

class HomeForm(forms.Form):
    post = forms.CharField(widget=forms.TextInput(
            attrs={
                    'class': 'form control form-control-lg',
                    'placeholder': 'Paste the URL to the Aliexpress product you want to import...'
                    }

            ))