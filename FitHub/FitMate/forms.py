from django import forms
from .models import CustomUser, Enrollment, UserProfile


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    # Override the form's clean method to check if password and confirm password match
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields='__all__'


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address', 'dob', 'gender',
            'emergency_contact_name', 'emergency_contact_phone', 'agreement',
            'joining_date', 'payment_status', 'membership_plan', 'trainer',
            'price', 'due_date'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }