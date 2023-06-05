from django.urls import path, include
from django.conf.urls.static import static
from BlogsProject import settings

from . import views


urlpatterns = [
    path("", views.get_main_page, name="main"),
    path("detail/<int:id>", views.get_detail, name="detail"),
    path("logIn/", views.logIn, name="log-in"),
    path("signUp/", views.signUp, name="sign-up"),
    path("logOut/", views.logOut, name="log-out"),
    path("category/<slug:slug>/", views.get_article_by_category, name="category"),
    path("category/<int:id>", views.add_to_watchlist, name="add"),
    path("watchlist/", views.get_watchlist_categories, name="watchlist"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
