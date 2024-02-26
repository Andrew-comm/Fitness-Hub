from django import forms
from .models import CustomUser, Enrollment, UserProfile, Session, Post, Comment


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude = ['user'] 


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address', 'dob', 'gender',
            'emergency_contact_name', 'emergency_contact_phone', 'agreement',
            'joining_date', 'payment_status', 'membership_plan', 'trainer'
           
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            
        }



class WorkoutSuggestionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'fitness_level',
            'fitness_goals',
            'workout_preferences',
            'nutritional_preferences',
            'age',
            'gender',
            'height',
            'weight',
            'medical_conditions',
            'medications',
            'allergies',
        ]




class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'description', 'video']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']