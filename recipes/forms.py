from django import forms
from .models import Recipe
from tinymce.widgets import TinyMCE


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "recipe_image",
            "category",
            "description",
            "ingredients",
            "instructions",
            "tags",
        ]
        widgets = {
            'description': TinyMCE(attrs={'style': 'width: 100%; height: 150px;'}),
            'ingredients': TinyMCE(attrs={'style': 'width: 100%; height: 300px;'}),
            'instructions': TinyMCE(attrs={'style': 'width: 100%; height: 300px;'}),
        }
