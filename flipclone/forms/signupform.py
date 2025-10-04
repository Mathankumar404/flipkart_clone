from django import forms
from flipclone.models import User
from django.contrib.auth.hashers import make_password

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "phone_no", "password"]

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")
        return make_password(password)  # hash before save
