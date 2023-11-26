
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from FitMate.forms import CustomUserCreationForm
from .models import UserProfile, Gallery, Enrollment, VirtualFitnessClass
from .forms import UserProfileForm, EnrollmentForm
from django.shortcuts import get_object_or_404
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder







def home(request):    
    profile = UserProfile.objects.all()  
    if request.user.is_authenticated:          
        profile = UserProfile.objects.get(user=request.user)    
    return render(request, 'home.html',{'profile':profile})

#view profile
User = get_user_model()

def view_profile(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.userprofile
    return render(request, 'profile.html', {'user': user, 'profile': profile})

def update_profile(request, pk):
    user = User.objects.get(pk=pk)

    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            return redirect('profile', pk=pk)  # Redirect to the 'view_profile' view
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

#create profile
@login_required
def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Associate the profile with the logged-in user
            profile.save()
            return redirect('view_profile', username=request.user.username)
    else:
        form = UserProfileForm()
    return render(request, 'profile.html', {'form': form})




#delete profile

def delete_profile(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile.delete()
        return redirect('home')
    return render(request, 'confirm_delete_profile.html')




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Authenticate and log in the user
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(f"Email: {email}, Password: {password}") 

        # Authenticate using email
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the 'home' view or URL name
        else:
            # Handle authentication failure
            return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('home')  





def Gallery_view(request):
    gallery = Gallery.objects.all()

    context = {'gallery':gallery}
    return render(request, 'gallery.html', context)

@login_required
def enrollment_form(request):
    # Check if the user already has an enrollment
    enrollment = get_object_or_404(Enrollment, user=request.user)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a success page
    else:
        # If the user doesn't have an enrollment, create a new form
        form = EnrollmentForm(instance=enrollment)

    return render(request, 'enrollment_form.html', {'form': form})


def virtual_classes(request):
    classes = VirtualFitnessClass.objects.all()
    context = {'classes': classes}
    return render(request, 'virtual_classes.html', context)

def suggest_workout(request):
    return render(request, 'workout_form.html')

def generate_workout(request):
    data = pd.read_csv("gym_data.csv")
    features = data[['age', 'height', 'weight', 'fitness_level', 'gender']]
    target = data['suggested_workout']

    # Fit the encoder for all categorical variables
    encoder = LabelEncoder()
    features['fitness_level'] = encoder.fit_transform(features['fitness_level'])
    features['gender'] = encoder.fit_transform(features['gender'])

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    if request.method == 'POST':
        # Extracting form data
        age = int(request.POST.get('age'))
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        fitness_level = request.POST.get('fitness_level')
        gender = request.POST.get('gender')

        # Encode categorical variables
        try:
            fitness_level_encoded = encoder.transform([fitness_level])[0]
        except ValueError:
            # If the fitness level is not in the encoder classes, use the first class
            fitness_level_encoded = encoder.transform([encoder.classes_[0]])[0]

        try:
            gender_encoded = encoder.transform([gender])[0]
        except ValueError:
            # If the gender is not in the encoder classes, use the first class
            gender_encoded = encoder.transform([encoder.classes_[0]])[0]

        # Predict workout
        workout_prediction = model.predict([[age, height, weight, fitness_level_encoded, gender_encoded]])[0]

        # Check if there are similar workouts in the CSV
        close_workouts = target[(target == workout_prediction)]
        if not close_workouts.empty:
            suggestion = f"We suggest: {workout_prediction}"
        else:
            suggestion = f"No similar workout found. Suggested workout: {workout_prediction}"

        return render(request, 'workout_result.html', {'workout_suggestion': suggestion})

    return render(request, 'workout_form.html')