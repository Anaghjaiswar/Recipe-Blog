from django.db import models
from django.conf import settings  # Use settings to reference the custom user model
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from django.utils.html import mark_safe
from tinymce.models import HTMLField
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')  # Use custom user model
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique_with='user__email')
    recipe_image = CloudinaryField('media', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='recipes')
    description = HTMLField()  
    ingredients = HTMLField()  
    instructions = HTMLField()  
    tags = TaggableManager(blank=True) 
    view_count = models.PositiveIntegerField(default=0)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="favorite_recipes", blank=True)  # Use custom user model
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.first_name}"

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['view_count']),
            models.Index(fields=['created_at']),
        ]
