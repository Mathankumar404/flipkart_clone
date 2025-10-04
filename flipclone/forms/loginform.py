from django import forms

class loginform(forms.Form):
    identifier = forms.CharField(
        max_length=150,
        label="Username or Phone Number",
        widget=forms.TextInput(attrs={"placeholder": "Enter username or mobile"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )
