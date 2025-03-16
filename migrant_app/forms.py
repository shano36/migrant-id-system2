from django import forms
from django.contrib.auth.models import User
from .models import MigrantWorker
from .models import Application
class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # ✅ Ensure email is collected
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # ✅ Include email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # ✅ Hash password correctly
        if commit:
            user.save()
        return user


class MigrantWorkerForm(forms.ModelForm):
    class Meta:
        model = MigrantWorker
        fields = ['full_name', 'aadhaar_number', 'email', 'phone_number', 'work_location']  # ✅ Added email

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "aadhaar_number", "email", "phone"]  # ✅ Ensure fields are correct