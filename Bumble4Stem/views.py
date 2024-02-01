from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest,HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from Bumble4Stem.models import Users, Matches, Rejected
from .forms import NewUserForm
# Create your views here.

def index(request):
    return render(request, "index.html")

def matching(request):
    if request.method["POST"]:
        if request.POST["like"]:
            m1id = request.session["user_id"]
            m2id = request.POST["like"]
            m = Matches(m1id=m1id, m2id=m2id)
            m.save()
            return HttpResponseRedirect("/matching")
        if request.POST["dislike"]:
            r1id = request.session["user_id"]
            r2id = request.POST["dislike"]
            r = Rejected(r1id=r1id, r2id=r2id)
            r.save()
            return HttpResponseRedirect("/matching")

    if request.method["GET"]:
        users = Users.objects.all()

        return render(request, "matching.html", context={"users": users})
    return render(request, "matching.html")

def myMatches(request):
    # SELECT m2id_id AS user2
    # FROM Bumble4Stem_matches
    # WHERE (m1id_id, m2id_id) IN (SELECT m2id_id, m1id_id FROM Bumble4Stem_matches) AND m1id_id = request.session["user_id"];
    return render(request, "myMatches.html")

def login(request):
    """Log user in"""

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            rows = Users.objects.get(email=email)
            request.session["user_id"] = rows.id
            user = authenticate(username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "login.html", context={"form": form})

def register(request):
    """Register user"""
    if request.method == "POST":
        form = NewUserForm(request.POST)
        display_name = request.POST['display_name']
        age = request.POST['age']
        batch = request.POST['batch']
        phn_no = request.POST['phn_no']
        pronouns = request.POST['pronouns']
        research_interests = request.POST['research_interests']
        bio = request.POST['bio']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        email = request.POST['email']
        users = Users.objects.values('email')
        for user in users:
            if user['email'] == email:
                messages.error(
                    request, "Account with email ID already exists")
                return render(request, "register.html", context={
                    "display_name": display_name,
                    "age": age,
                    "batch": batch,
                    "phn_no": phn_no,
                    "pronouns": pronouns,
                    "research_interests": research_interests,
                    "bio": bio,
                    "email": email,
                    })
        if pass1 != pass2:
            messages.error(
                request, "Passwords do not match")
            return HttpResponseRedirect("register")
        if len(pass1) < 8:
            messages.error(
                request, "Passwords should have at least 8 characters")
            return HttpResponseRedirect("register")
        if form.is_valid():
            user = form.save()
            f = Users( 
                email=email,
                display_name=display_name,
                age=age,
                batch=batch,
                phn_no=phn_no,
                pronouns=pronouns,
                research_interests=research_interests,
                bio=bio)
            f.save()
            rows = Users.objects.get(email=user.email)
            request.session["user_id"] = rows.id
            auth_login(request, user)
            return HttpResponseRedirect("/")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "register.html", context={"register_form": form})


def logout(request):
    """Log user out"""

    logout_user(request)
    return HttpResponseRedirect("/")

def handler404(request, exception):
    return HttpResponseNotFound(request, '404.html')


def handler500(request):
    return HttpResponseServerError(request, '500.html')


def handler403(request, exception):
    return HttpResponseForbidden(request, '403.html')


def handler400(request, exception):
    return HttpResponseBadRequest(request, '400.html')


def csrf_failure(request, reason=""):
    
    return render(request,'403_csrf.html')