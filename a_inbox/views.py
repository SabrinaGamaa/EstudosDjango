from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def inbox_view(request):
    return render(request, 'a_inbox/inbox.html')
