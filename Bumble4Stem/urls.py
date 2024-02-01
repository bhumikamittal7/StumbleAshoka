from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/",views.logout, name="logout"),
    path("matching/", views.matching, name="matching"),
    path("myMatches/", views.myMatches, name="myMatches")
]


handler404 = "Bumble4Stem.views.handler404"
handler400 = "Bumble4Stem.views.handler400"
handler500 = "Bumble4Stem.views.handler500"
handler403 = "Bumble4Stem.views.handler403"