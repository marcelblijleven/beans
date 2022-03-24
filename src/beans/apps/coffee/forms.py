from django import forms


class AddCoffeeForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    country = forms.CharField(max_length=80, required=True)
    processing = forms.CharField(required=True)
    roaster = forms.CharField(max_length=200)
    roasting_date = forms.DateField(required=True)
    rating = forms.IntegerField(required=False)
