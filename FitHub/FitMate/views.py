from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from FitMate.forms import CustomUserCreationForm
from .models import UserProfile
from .forms import UserProfileForm


def home(request):
    profile = UserProfile.objects.get(user=request.user)    
    return render(request, 'home.html',{'profile':profile})

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


#update profile
@login_required
def update_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            return redirect('view_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

#view profile
User = get_user_model()

def view_profile(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.userprofile
    return render(request, 'profile.html', {'user': user, 'profile': profile})
#delete profile
@login_required
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
