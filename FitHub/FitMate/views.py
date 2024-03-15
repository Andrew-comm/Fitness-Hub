
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.db.models import Count, Case, When, IntegerField,Sum, CharField, Value

import json
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from FitMate.forms import CustomUserCreationForm
from .models import CustomUser, UserProfile, Gallery, Enrollment, VirtualFitnessClass,Trainer, MembershipPlan,Post, Session, Like, ProgressData, AwardLevel
from twilio.rest import Client
from django.conf import settings
from .forms import UserProfileForm, EnrollmentForm, SessionForm, PostForm, CommentForm, ProgressForm
from django.shortcuts import get_object_or_404
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder





@login_required
def home(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    # Fetch gallery objects
    gallery = Gallery.objects.all()

    return render(request, 'home.html', {'profile': profile, 'gallery': gallery})

#view profile
@login_required
def view_profile(request):
    try:
        profile = request.user.userprofile
        return render(request, 'profile.html', {'profile': profile})
    except UserProfile.DoesNotExist:
        # Redirect to create profile view
        return redirect('create_profile')
    


@login_required
def create_profile(request):
    try:
        profile = request.user.userprofile
        return redirect('profile')  # Redirect if profile already exists
    except UserProfile.DoesNotExist:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('profile')  # Redirect to the user's profile without any additional parameters
        else:
            form = UserProfileForm()
        return render(request, 'create_profile.html', {'form': form})

@login_required
def update_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})


@login_required
def delete_profile(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    profile.delete()
    return redirect('home')




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
    if request.user.is_authenticated:
        logout(request)  # Logout any user already logged in
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # print(f"Email: {email}, Password: {password}") 

        # Authenticate using email
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the previous page or 'home' if not available
            return redirect(request.GET.get('next', 'home'))  
        else:
            # Handle authentication failure
            error_message = "Invalid email or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('home')  


@login_required
def enrollment_form(request):
    # Check if the user already has an enrollment
    enrollment_instance = Enrollment.objects.filter(user=request.user).first()
    enrollment_exists = enrollment_instance is not None

    if request.method == 'POST':
        if enrollment_instance:
            # Update existing enrollment with the new form data
            form = EnrollmentForm(request.POST, instance=enrollment_instance)
        else:
            # Create a new enrollment if none exists
            form = EnrollmentForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()

             # Get the phone number from the form
            phone_number = form.cleaned_data['phone']
            
            # Send SMS notification
            send_sms_notification(phone_number)
            return redirect('home')  # Redirect to home page after successful enrollment
    else:
        # If the user is enrolled, pre-fill the form with their data
        if enrollment_instance:
            form = EnrollmentForm(instance=enrollment_instance)
        else:
            form = EnrollmentForm()

    membership_plans = MembershipPlan.objects.all()
    trainers = Trainer.objects.all()

    return render(request, 'enrollment_form.html', {'form': form, 'membership_plans': membership_plans, 'trainers': trainers, 'enrollment_exists': enrollment_exists})

def send_sms_notification(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body="Congratulations! You have successfully enrolled in  gymgenius.",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

@login_required
def virtual_classes(request):
    classes = VirtualFitnessClass.objects.all()
    context = {'classes': classes}
    return render(request, 'virtual_classes.html', context)

def suggest_workout(request):
    return render(request, 'workout_form.html')


@login_required
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




def community_feed_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'community_feed.html', {'posts': posts})

def community_feed_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('community_feed_list')  # Redirect to list view after success
    else:
        form = PostForm()
    return render(request, 'community_feed_create.html', {'form': form})



def record_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('community_feed')
    else:
        form = SessionForm()
    return render(request, 'record_session.html', {'form': form})




def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('community_feed')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'post': post})


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # Check if the user has already liked the post
    if request.method == 'POST':
        user = request.user
        if Like.objects.filter(post=post, user=user).exists():
            # If the user has already liked the post, do nothing (can be used to unlike later)
            pass
        else:
            # If the user has not liked the post, create a new Like instance
            Like.objects.create(post=post, user=user)
    return redirect('community_feed')


@login_required
def log_progress(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # If the UserProfile does not exist, create it
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress_data = form.save(commit=False)
            progress_data.user = request.user  # Assign the logged-in user to the ProgressData instance
            progress_data.save()  # Save the ProgressData object
            
            # Award points to the user for logging progress
            user_profile.points += 10  # Award 10 points for each row logged
            user_profile.save()

            return redirect('dashboard')  # Redirect to a success page after logging progress
    else:
        form = ProgressForm()
    
    return render(request, 'log_progress.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    progress_data = ProgressData.objects.filter(user=user).order_by('date')

    # Convert dates to strings for JSON serialization (avoid potential date format issues)
    weight_labels = [data.date.strftime('%Y-%m-%d') for data in progress_data]
    weight_data = [data.weight_kg for data in progress_data]
    calories_labels = [data.date.strftime('%Y-%m-%d') for data in progress_data]
    calories_data = [data.calories_burned for data in progress_data]

    context = {
        'progress_data': progress_data,
        'weight_labels': weight_labels,  # Added
        'weight_data': weight_data,  # Added
        'calories_labels': calories_labels,  # Added
        'calories_data': calories_data,  # Added
    }
    return render(request, 'dashboard.html', context)




@login_required
def awards_page(request):
    # Fetch all award levels from the database
    award_levels = AwardLevel.objects.all()

    # Create a list of dictionaries for award levels to use in the view
    award_levels_data = [
        {"name": level.name, "min_points": level.min_points}
        for level in award_levels
    ]

    # Annotate users with their total points and assign award levels
    users = CustomUser.objects.annotate(
        total_points=Sum('userprofile__points')
    ).annotate(
        award_level=Case(
            *[When(total_points__gte=level['min_points'], then=Value(level['name'])) for level in award_levels_data],
            default=Value("No Award"), output_field=CharField()
        )
    ).order_by('-total_points')

    context = {'users': users}
    return render(request, 'awards_page.html', context)



def award_details(request, award_level):   
    
    # Retrieve award details based on the award level
    try:
        award_level_obj = AwardLevel.objects.get(name=award_level)
    except AwardLevel.DoesNotExist:
        return render(request, 'award_not_found.html')

    context = {'award_level': award_level_obj}
    return render(request, 'award_details.html', context)


def award_list(request):
    awards = AwardLevel.objects.all()
    return render(request, 'award_list.html', {'awards': awards})
