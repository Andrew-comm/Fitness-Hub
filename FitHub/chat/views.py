from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required

@login_required(login_url='FitMate:login')
def chat_room(request):
    return render(request, 'chat.html', {})
