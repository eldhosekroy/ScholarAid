from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'username',         # For login
            'phone',
            'email',
            'address',
            'place',
            'district',
            'school',
            'student_class',
            'financial_status',
            'photo',
            'password',
        ]




class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class SponsorRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = StudentProfile
        fields = [
            'username',
            'email',
            'org_address',
            'district',
            'org_name',
            'place',
            'org_license',
            'password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if pwd and confirm and pwd != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

