from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from . import forms
from .models import Articles, UserAccount, Categories, WatchListCategories


def get_main_page(request):
    queryset_articles = Articles.objects.all().order_by("created_at")
    queryset_categories = Categories.objects.all()
    template = "index.html"
    context = {"articles_data": queryset_articles, "categories": queryset_categories}

    return render(request, template, context)


def get_article_by_category(request, slug):
    category = get_object_or_404(Categories, slug=slug)
    queryset_articles = category.articles.all()
    queryset_categories = Categories.objects.all()
    context = {"articles_data": queryset_articles, "categories": queryset_categories}
    template = "index.html"

    return render(request, template, context)


def get_detail(request, id: int):
    content = Articles.objects.get(id=id)
    queryset_categories = Categories.objects.all()
    template = "detail.html"
    context = {"content": content, "categories": queryset_categories}

    return render(request, template, context)


def get_watchlist_categories(request):
    watchlist = WatchListCategories.objects.get(user=request.user).category.all()
    context = {"watchlist": watchlist}
    tempalte = "watchlist.html"

    print(watchlist)

    return render(request, tempalte, context)


@login_required(login_url="/logIn/")
def add_to_watchlist(request, id):
    try:
        watchlist = WatchListCategories.objects.get(user=request.user)
    except ObjectDoesNotExist:
        watchlist = WatchListCategories(user=request.user)
        watchlist.save()

    finally:
        watchlist.category.add(id)

    return HttpResponseRedirect(reverse("watchlist"))


def logIn(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            useraccount = UserAccount.objects.get(email=email)

            user = authenticate(useremail=useraccount.get_username(), password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("main"))
            else:
                return HttpResponse("User Not Found")
        except ObjectDoesNotExist:
            return HttpResponse("User Not Found")

    return render(request, "logInPage.html", {"form": forms.UserLogInForm()})


def signUp(request):
    if request.method == "POST":
        form = forms.UserSignUpForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(
                commit=False
            )  # Get the unsaved user instance from the form

            # Hash the password
            password = form.cleaned_data.get("password")
            hashed_password = make_password(password)
            user.password = hashed_password

            user.save()

        return HttpResponseRedirect(reverse("log-in"))

    return render(request, "signUpPage.html", {"form": forms.UserSignUpForm})


def logOut(request):
    logout(request)
    print(request.user.is_authenticated)
    return HttpResponseRedirect(reverse("log-in"))
