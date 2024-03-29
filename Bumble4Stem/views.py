from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest,HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django_ratelimit.decorators import ratelimit

from Bumble4Stem.models import Users, Matches, Rejected
from django.db.models import Q, F
from .forms import NewUserForm, CaptchaForm
import datetime
# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required(login_url='/login')
def profile(request):
    user = Users.objects.filter(id=request.session["user_id"]).first()
    return render(request, "myProfile.html", context={"fuser": user})

@login_required(login_url='/login')
def otherProfile(request, id):
    user = Users.objects.filter(id=id).first()
    return render(request, "otherProfile.html", context={"fuser": user})

@login_required(login_url='/login')
def matching(request):
    if request.method == "POST":
        print(list(request.POST.keys())[1])
        if list(request.POST.keys())[1] == "like":
            m1id = Users.objects.filter(id=request.session["user_id"]).first()
            m2id = Users.objects.filter(id=request.POST["like"]).first()
            m = Matches(m1id=m1id, m2id=m2id)
            m.save()
            return HttpResponseRedirect("/matching")

        if list(request.POST.keys())[1] == "dislike":
            r1id = Users.objects.filter(id=request.session["user_id"]).first()
            r2id = Users.objects.filter(id=request.POST["dislike"]).first()
            r = Rejected(r1id=r1id, r2id=r2id)
            r.save()
            return HttpResponseRedirect("/matching")

    if request.method == "GET":
        user= getRandomUser(request.session["user_id"])
        if user != None:
            return render(request, "matching.html", context={"fuser": user})
        else:
            return render(request, "matching.html", context={"fuser": "user not found"})
    
    return render(request, "matching.html")

@login_required(login_url='/login')
def myMatches(request):
    likes = Matches.objects.filter(m1id=request.session['user_id']).values('m2id')
    matches = []
    for like in likes:
        m = Matches.objects.filter(Q(m1id=like["m2id"], m2id=request.session["user_id"])
        ).values('m2id')
        if m.exists():
            matches.append(like["m2id"])

    user2_list = Users.objects.filter(id__in=matches)
    return render(request, "myMatches.html", context={"matches": list(user2_list)})

@login_required(login_url='/login')
def myLikes(request):
    if request.method == "POST":
        if list(request.POST.keys())[1] == "like":
            m1id = Users.objects.filter(id=request.session["user_id"]).first()
            m2id = Users.objects.filter(id=request.POST["like"]).first()
            m = Matches(m1id=m1id, m2id=m2id)
            m.save()
            return HttpResponseRedirect("/myLikes")

        if list(request.POST.keys())[1] == "dislike":
            r1id = Users.objects.filter(id=request.session["user_id"]).first()
            r2id = Users.objects.filter(id=request.POST["dislike"]).first()
            r = Rejected(r1id=r1id, r2id=r2id)
            r.save()
            return HttpResponseRedirect("/myLikes")
    if request.method == "GET":
        matches= getMatches(request.session["user_id"])
        rejects= getRejects(request.session["user_id"])
        
        likes = Matches.objects.filter(m2id=request.session["user_id"]).exclude(m1id__in=matches).exclude(m1id__in=rejects).values('m1id')
        likes = [like['m1id'] for like in likes]
        user2_list = Users.objects.filter(id__in=likes)
        
        return render(request, "myLikes.html", context={"likes": list(user2_list)})

@login_required(login_url='/login')
def editProfile(request):
    if request.method == "POST":
        avatar_index = request.POST['avatar_index']
        batch = request.POST['batch']
        pronouns = request.POST['pronouns']
        major = request.POST['major']
        research_interests = request.POST['research_interests']
        Q1 = request.POST['Q1']
        Q2 = request.POST['Q2']
        Q3 = request.POST['Q3']
        id = request.session['user_id']

        user = Users.objects.get(id=id)
        user.avatar_index = avatar_index
        user.batch = batch
        user.pronouns = pronouns
        user.major = major
        user.research_interests = research_interests
        user.Q1 = Q1
        user.Q2 = Q2
        user.Q3 = Q3
        user.save(update_fields=["avatar_index", 'batch', 'pronouns', 'major', 'research_interests', 'Q1', 'Q2', 'Q3'])
        return HttpResponseRedirect("/myProfile")
    if request.method == "GET":
        user = Users.objects.filter(id=request.session["user_id"]).first()
        return render(request, "editProfile.html", context={
            "fuser": user
            })


@ratelimit(key='ip', rate='2/m', method='POST')
def login(request):
    """Log user in"""

    if request.method == "POST":
        captcha = CaptchaForm(request.POST)
        if not captcha.is_valid():
            messages.error(request, "Invalid captcha")
        else:
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
    cap = CaptchaForm()
    return render(request, "login.html", context={"form": form, "CaptchaForm": cap})

@ratelimit(key='ip', rate='4/m', method="POST")
def register(request):
    """Register user"""
    if request.method == "POST":
        captcha = CaptchaForm(request.POST)
        if not captcha.is_valid():
            messages.error(request, "Invalid captcha")
            return render(request, "register.html", context={
                        "display_name": request.POST['display_name'],
                        "batch": request.POST['batch'],
                        "major": request.POST['major'],
                        "pronouns": request.POST['pronouns'],
                        "research_interests": request.POST['research_interests'],
                        "Q1": request.POST['Q1'],
                        "Q2": request.POST['Q2'],
                        "Q3": request.POST['Q3'],
                        "email": request.POST['email'],
                        "avatar_index": request.POST['avatar_index'],
                        "CaptchaForm": CaptchaForm()
                        })
        else:
            form = NewUserForm(request.POST)
            display_name = request.POST['display_name']
            batch = request.POST['batch']
            pronouns = request.POST['pronouns']
            major = request.POST['major']
            research_interests = request.POST['research_interests']
            Q1 = request.POST['Q1']
            Q2 = request.POST['Q2']
            Q3 = request.POST['Q3']
            pass1 = request.POST['password1']
            pass2 = request.POST['password2']
            email = request.POST['email']
            avatar_index = request.POST['avatar_index']
            users = Users.objects.values('email')
            for user in users:
                if user['email'] == email:
                    messages.error(
                        request, "Account with email ID already exists")
                    return render(request, "register.html", context={
                        "display_name": display_name,
                        "batch": batch,
                        "major": major,
                        "pronouns": pronouns,
                        "research_interests": research_interests,
                        "Q1": Q1,
                        "Q2": Q2,
                        "Q3": Q3,
                        "email": email,
                        "avatar_index": avatar_index,
                        "CaptchaForm": CaptchaForm()
                        })
            if pass1 != pass2:
                messages.error(
                    request, "Passwords do not match")
                return render(request, "register.html", context={
                        "display_name": display_name,
                        "batch": batch,
                        "major": major,
                        "pronouns": pronouns,
                        "research_interests": research_interests,
                        "Q1": Q1,
                        "Q2": Q2,
                        "Q3": Q3,
                        "email": email,
                        "avatar_index": avatar_index,
                        "CaptchaForm": CaptchaForm()
                        })
            if len(pass1) < 8:
                messages.error(
                    request, "Passwords should have at least 8 characters")
                return render(request, "register.html", context={
                        "display_name": display_name,
                        "batch": batch,
                        "major": major,
                        "pronouns": pronouns,
                        "research_interests": research_interests,
                        "Q1": Q1,
                        "Q2": Q2,
                        "Q3": Q3,
                        "email": email,
                        "avatar_index": avatar_index,
                        "CaptchaForm": CaptchaForm()
                        })
            if form.is_valid():
                user = form.save()
                f = Users( 
                    email=email,
                    display_name=display_name,
                    major=major,
                    batch=batch,
                    pronouns=pronouns,
                    research_interests=research_interests,
                    Q1=Q1,
                    Q2=Q2,
                    Q3=Q3,
                    avatar_index=avatar_index)
                f.save()
                rows = Users.objects.get(email=user.email)
                request.session["user_id"] = rows.id
                auth_login(request, user)
                return HttpResponseRedirect("/")
            messages.error(request, "Follow the password rules")
            return render(request, "register.html", context={
                        "display_name": display_name,
                        "batch": batch,
                        "major": major,
                        "pronouns": pronouns,
                        "research_interests": research_interests,
                        "Q1": Q1,
                        "Q2": Q2,
                        "Q3": Q3,
                        "email": email,
                        "avatar_index": avatar_index,
                        "CaptchaForm": CaptchaForm()
                        })
    form = NewUserForm()
    cap = CaptchaForm()
    return render(request, "register.html", context={"register_form": form, "CaptchaForm": cap})


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

def getRandomUser(id):
    """Get a random user"""
    matches = Matches.objects.filter(m1id=id).values('m2id')
    rejects = Rejected.objects.filter(r1id=id).values('r2id')
    # Extracting user IDs from matches and rejects
    matched_user_ids = [match['m2id'] for match in matches]
    rejected_user_ids = [reject['r2id'] for reject in rejects]
    
    # Combine the lists of excluded user IDs
    excluded_user_ids = matched_user_ids + rejected_user_ids

    # Get a random user
    user = Users.objects.exclude(id=id).exclude(id__in=excluded_user_ids).order_by('?').first()
    return user

def getMatches(id):
    likes = Matches.objects.filter(m1id=id).values('m2id')
    matches = []
    for like in likes:
        m = Matches.objects.filter(Q(m1id=like["m2id"], m2id=id)
        ).values('m2id')
        if m.exists():
            matches.append(like["m2id"])
    return matches

def getRejects(id):
    rejects = Rejected.objects.filter(r1id=id).values('r2id')
    return [reject['r2id'] for reject in rejects]
