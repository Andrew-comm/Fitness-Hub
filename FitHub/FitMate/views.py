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