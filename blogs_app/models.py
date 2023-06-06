from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.urls import reverse

from BlogsProject.settings import MEDIA_ROOT


class UserAccount(AbstractUser):
    # Required
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        blank=False, null=False, max_length=255, validators=[username_validator]
    )
    image = models.ImageField(upload_to=f"{MEDIA_ROOT}/authors_image/")
    email = models.EmailField(("email address"), unique=True, blank=False)
    password = models.CharField(("password"), max_length=255)
    first_name = models.CharField(("first name"), max_length=100)
    last_name = models.CharField(("last name"), max_length=100)
    is_superuser = models.BooleanField(blank=False, null=False, default=False)
    is_staff = models.BooleanField(blank=False, null=False, default=False)
    is_active = models.BooleanField(blank=False, null=False, default=False)

    # Make invisible all optional fields
    last_login = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_users", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "password",
        "image",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
    ]

    class Meta:
        ordering = ["first_name"]
        default_permissions = ()

    def __str__(self) -> str:
        return str(self.first_name)


class Articles(models.Model):
    title = models.CharField(max_length=100, unique=True, default="")
    summarises = models.TextField(validators=[MinLengthValidator(170)])
    image = models.ImageField(upload_to=f"{MEDIA_ROOT}/images/")
    images_title = models.ManyToManyField("ImagesTitle", related_name="articles")
    categories = models.ManyToManyField("Categories", related_name="articles")
    author = models.ManyToManyField(UserAccount, related_name="articles")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return str(self.title)


class ImagesTitle(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return str(self.title)


class Categories(models.Model):
    category_name = models.CharField(max_length=100, unique=True, default="")
    slug = models.SlugField(default="undecided", unique=True)

    def get_absolute_url(self) -> str:
        return reverse("category", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return str(self.category_name)


class Comments(models.Model):
    article = models.ForeignKey(
        Articles, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(default="undecided")

    def __str__(self) -> str:
        return str(self.author)


class WatchListCategories(models.Model):
    user = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="watchlist_categories",
    )

    category = models.ManyToManyField(Categories, related_name="watch_categories")

    def __str__(self) -> str:
        return str(self.user)
