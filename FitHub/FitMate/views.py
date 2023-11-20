from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from FitMate.forms import CustomUserCreationForm
from .models import UserProfile, Gallery, Enrollment
from .forms import UserProfileForm, EnrollmentForm
from django.shortcuts import get_object_or_404





def home(request):
    gallery = Gallery.objects.all()
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