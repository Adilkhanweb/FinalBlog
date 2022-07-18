from django.db import models
# Gives access to all needed fields like username, password, email
from django.contrib.auth.models import AbstractUser, User
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify


# Category model
class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField()

    def save(self, *args, **kwargs, ):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def save(self, *args, **kwargs, ):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={
            'slug': self.slug
        })

    def get_like_url(self):
        return reverse("like", kwargs={
            'slug': self.slug
        })

    def get_thumbnail(self):
        if self.thumbnail is not None:
            return mark_safe('<img src="{}" height="50" >'.format(self.thumbnail.url))
        else:
            return ""

    # When we are specifying as property,
    # we can call it easily in the htm file
    @property
    def comments(self):
        return self.comment_set.all()

    # Adding method to count how many comments are there
    @property
    def get_comment_count(self):
        return self.comment_set.all().count()

    @property
    def get_view_count(self):
        return self.postview_set.all().count()

    @property
    def get_like_count(self):
        return self.like_set.all().count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Every comment need to be related to a post, so we specify the post as foreignkey
    # CASCADE : When the post is deleted the comment is deleted
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
