from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from szchober.models import UserProfile
from szchober.forms import UserFormDriver, UserFormRider, UserProfileForm, FeedbackForm

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

'''
----------------------------------------------------------------------------------------------------------------
 views.py file - registers the web apps views for the urls. creates views for:
    - index
    - sign up
    - become a rider 
    - become a driver
    - find a lift
    - account, driver
    - account, rider
    - about us
    - login
    - logout
    - feedback
----------------------------------------------------------------------------------------------------------------
'''


def index(request):
    return render(request, 'szchober/index.html')


def sign_up(request):
    return render(request, 'szchober/sign-up.html')


def become_rider(request):
    registered = False
    if request.method == 'POST':
        user_form = UserFormRider(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserFormRider()
        profile_form = UserProfileForm()

    return render(request,
                  'szchober/become-a-rider.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def become_driver(request):
    registered = False
    if request.method == 'POST':
        user_form = UserFormDriver(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserFormDriver()
        profile_form = UserProfileForm()

    return render(request,
                  'szchober/become-a-driver.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def myAccount_rider(request):
    return HttpResponse("this is my rider account")


def myAccount_driver(request):
    return HttpResponse("this is my driver account")


def find_lift(request):
    return render(request, 'szchober/find-a-lift.html')


def about(request):
    return render(request, 'szchober/about-us.html')


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,"Feedback Submitted Sucessfully")
    else:
        form = FeedbackForm()

    return render(request, 'szchober/feedback.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('szchober:index'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print("Invalid login details")
            return HttpResponse("Invalid login details supplied" + "<br><a href='/szchober/'>Homepage</a>")
    else:
        return render(request, 'szchober/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('szchober:index'))
