# Models

## Articles

- summarises = models.TextField()
- title= models.CharField(unique=True)
- image = models.ImageField()
- images_title = models.ManyToMany(ImagesTitle, related_name="articles")
- categories = models.ManyToMany(Categories, related_name="articles")
- created_at = models.DateTimeField(auto_now_add=True)

## ImagesTitle

- title = CharField(max_length=100, min_length=6, unique=True)

## Categories

- category_name = CharField(max_length=100)
- slug = SlugField(default="undecided")

## UserAccount

- email = CharField(max_length=100, min_length=6)
- password = CharField(max_length=100, min_length=6)
- lastname_name = CharField(max_length=100, min_length=6, unique=True)
- firist_name = CharField(max_length=100, min_length=6, unique=True)
- sur_name = CharField(max_length=100, min_length=6, unique=True)
- image = ImageField(blank=True, null=True)

## Comments

- article = ForeignKey(Articles, on_delete=models.CASCADE, related_name="comments")
- author = ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
- comment = TextField(default="undecided")

# Views
