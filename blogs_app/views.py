from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from . import forms
from .models import Articles, UserAccount, Categories, WatchListCategories, Comments


def get_main_page(request):
    queryset_articles = Articles.objects.all().order_by("created_at")
    queryset_categories = Categories.objects.all()
    template = "index.html"
    context = {
        "articles_data": queryset_articles,
        "categories": queryset_categories,
    }

    if request.method == "POST":
        q = request.POST["q"]
        queryset_articles = Articles.objects.filter(title__contains=q)
        context["articles_data"] = queryset_articles

        print(context)

        return render(request, template, context)

    return render(request, template, context)


def get_article_by_category(request, slug):
    category = get_object_or_404(Categories, slug=slug)
    queryset_articles = category.articles.all()
    queryset_categories = Categories.objects.all()
    context = {"articles_data": queryset_articles, "categories": queryset_categories}
    template = "index.html"

    return render(request, template, context)


@login_required(login_url="/logIn/")
def get_detail(request, id: int):
    content = Articles.objects.get(id=id)
    queryset_categories = Categories.objects.all()
    comments = Comments.objects.filter(article=id)
    form = forms.AddComment(article=content, user=request.user)
    template = "detail.html"
    context = {
        "content": content,
        "categories": queryset_categories,
        "form": form,
        "comments": comments,
    }

    return render(request, template, context)


def add_comment(request, id: int):
    if request.method == "POST":
        article = Articles.objects.get(id=id)
        user = request.user

        Comments(article=article, author=user, content=request.POST["content"]).save()
        return HttpResponseRedirect(reverse("detail", kwargs={"id": id}))

    return HttpResponseRedirect(reverse("detail", kwargs={"id": id}))


def get_watchlist_categories(request):
    try:
        watchlist = WatchListCategories.objects.get(user=request.user).category.all()
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("main"))
    else:
        context = {"watchlist": watchlist}
        tempalte = "watchlist.html"

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


@login_required(login_url="/logIn/")
def leave_article(request):
    template = "leaveArticles.html"

    if request.method == "POST":
        form = forms.LeaveArticles(request.POST, request.FILES)
        context = {"form": form, "message": form.errors}

        if form.is_valid():
            form.save()

        return render(request, template, context)

    form = forms.LeaveArticles()
    context = {"form": form, "message": form.errors}

    return render(request, template, context)


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
    return HttpResponseRedirect(reverse("log-in"))
