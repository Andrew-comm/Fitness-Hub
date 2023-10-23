from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from FitMate.forms import CustomUserCreationForm

def home(request):
    return render(request, 'home.html')

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
        email = request.POST['email']  # Use 'email' instead of 'username'
        password = request.POST['password']

        # Create a user variable to store the user object
        user = None

        # Authenticate using email
        if email and password:
            user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Handle authentication failure
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')